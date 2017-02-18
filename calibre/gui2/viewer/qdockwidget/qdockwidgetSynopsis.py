from PyQt5.QtCore import QPoint
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget

from calibre.ebooks import markdown
from calibre.gui2.viewer.qdialog.qdialogConfig import config
from calibre.gui2.viewer.qdockwidget.qdockwidget import Qdockwidget
from calibre.library.filepath import filepath_relative

I = I


class QdockwidgetSynopsis(Qdockwidget):
    def __init__(self, *args, **kwargs):
        super(QdockwidgetSynopsis, self).__init__(*args, **kwargs)

        self.path_source = None
        self.synopsis_extension = None
        self.mono_family = None
        self.default_font_size = None
        self.qwebviewPreview_scroll = None
        self.qplaintexteditSynopsis_scroll = None

        self.setTitleBarWidget(QWidget())
        self.titleBarWidget_default = self.titleBarWidget()

        self.update_config()

        self.toolButtonRedo.setIcon(QIcon(I("edit-redo.png")))
        self.toolButtonUndo.setIcon(QIcon(I("edit-undo.png")))
        self.toolButtonSave.setIcon(QIcon(I("save.png")))
        self.toolButtonPreview.setIcon(QIcon(I("beautify.png")))
        self.toolButtonReload.setIcon(QIcon(I("view-refresh.png")))

        self.qwebviewPreview.page().mainFrame().contentsSizeChanged.connect(
            self.on_mainFrame_contentSizeChanged)
        self.qwebviewPreview.page().scrollRequested.connect(
            self.on_qwebviewPreview_scrollRequested
        )
        self.qplaintexteditSynopsis.verticalScrollBar().sliderMoved.connect(
            self.on_qplaintexteditSynopsis_sliderMoved
        )

    def on_qplaintexteditSynopsis_sliderMoved(self, value):
        p_height = self.qwebviewPreview.page().mainFrame().scrollBarMaximum(Qt.Vertical)
        s_height = self.qplaintexteditSynopsis.verticalScrollBar().maximum()

        s_position = self.qplaintexteditSynopsis.verticalScrollBar().sliderPosition()
        p_position = s_position * float(p_height) / s_height if s_position > 0 else 0

        self.qwebviewPreview.page().blockSignals(True)
        self.qwebviewPreview.page().mainFrame().setScrollPosition(QPoint(0, p_position))
        self.qwebviewPreview.page().blockSignals(False)

    def on_qwebviewPreview_scrollRequested(self, dx, dy, rectToScroll):
        p_height = self.qwebviewPreview.page().mainFrame().scrollBarMaximum(Qt.Vertical)
        s_height = self.qplaintexteditSynopsis.verticalScrollBar().maximum()

        p_position = self.qwebviewPreview.page().mainFrame().scrollPosition().y()
        s_position = p_position * float(s_height) / p_height if p_position > 0 else 0

        self.qplaintexteditSynopsis.verticalScrollBar().blockSignals(True)
        self.qplaintexteditSynopsis.verticalScrollBar().setValue(s_position)
        self.qplaintexteditSynopsis.verticalScrollBar().blockSignals(False)

    @pyqtSlot(bool)
    def on_toolButtonPreview_clicked(self, checked):
        self.preview()

    @pyqtSlot(bool)
    def on_qwebviewPreview_showEditor(self):
        self.edit()

    @pyqtSlot(bool)
    def on_qplaintexteditSynopsis_showPreview(self):
        self.preview()

    def on_mainFrame_contentSizeChanged(self, size):
        if not self.qwebviewPreview_scroll:
            return

        self.qwebviewPreview.page().mainFrame().setScrollBarValue(
            Qt.Vertical, self.qwebviewPreview_scroll)

    @pyqtSlot()
    def on_qplaintexteditSynopsis_contentChanged(self):
        if not self.qplaintexteditSynopsis_scroll:
            return

        self.qplaintexteditSynopsis.verticalScrollBar().setValue(
            self.qplaintexteditSynopsis_scroll)

    def preview(self):
        self.save()

        self.setTitleBarWidget(QWidget())
        self.stackedWidget.setCurrentIndex(1)

    def edit(self):
        self.setTitleBarWidget(self.titleBarWidget_default)
        self.stackedWidget.setCurrentIndex(0)
        self.qplaintexteditSynopsis.setFocus()

    def update_config(self):
        opts = config().parse()
        self.synopsis_extension = opts.synopsis_extension
        self.mono_family = opts.mono_family
        self.default_font_size = opts.default_font_size

        self.qplaintexteditSynopsis.setFont(QFont(self.mono_family))

    def toggle_preview(self, show):
        self.show()
        if show:
            self.preview()
        else:
            self.edit()

    def append(self, text):
        self.qplaintexteditSynopsis.appendPlainText(text)

        if self.stackedWidget.currentIndex():
            self.save()

    @pyqtSlot(bool)
    def on_qactionSave_triggered(self):
        self.save()

    @pyqtSlot(bool)
    def on_qactionPreview_triggered(self):
        self.preview()

    @pyqtSlot(bool)
    def on_qplaintexteditSynopsis_modificationChanged(self, changed):
        self.toolButtonSave.setEnabled(changed)

    @pyqtSlot(bool)
    def on_toolButtonRedo_clicked(self, checked):
        self.qplaintexteditSynopsis.redo()

    @pyqtSlot(bool)
    def on_toolButtonUndo_clicked(self, checked):
        self.qplaintexteditSynopsis.undo()

    @pyqtSlot(bool)
    def on_qplaintexteditSynopsis_redoAvailable(self, available):
        self.toolButtonRedo.setEnabled(available)

    @pyqtSlot(bool)
    def on_qplaintexteditSynopsis_undoAvailable(self, available):
        self.toolButtonUndo.setEnabled(available)

    @pyqtSlot(bool)
    def on_toolButtonReload_clicked(self, checked):
        self.load()

    @pyqtSlot(bool)
    def on_toolButtonSave_clicked(self, checked):
        self.save()

    def save(self):
        try:
            with open(self.path_synopsis(), "r+") as oput:
                self.write_to_file(oput)
        except IOError as error:
            if error.errno != 2:
                raise

            if not self.qplaintexteditSynopsis.toPlainText():
                return

            with open(self.path_synopsis(), "ab+") as oput:
                self.write_to_file(oput)

    def write_to_file(self, oput):
        text = self.qplaintexteditSynopsis.toPlainText()
        if text == oput.read():
            return

        oput.seek(0)
        oput.write(text)
        oput.truncate()

        self.update_scroll()
        self.load_preview(text)
        self.qplaintexteditSynopsis.document().setModified(False)

    def update_scroll(self):
        self.qplaintexteditSynopsis_scroll = self.qplaintexteditSynopsis.verticalScrollBar().value()
        self.qwebviewPreview_scroll = self.qwebviewPreview.page().mainFrame().scrollBarValue(
            Qt.Vertical)

    def set_path_source(self, path):
        self.path_source = path
        self.load()

    def path_synopsis(self):
        self.update_config()
        if not self.synopsis_extension:
            raise ValueError("synopsis extension unset")

        return filepath_relative(self.path_source, extension=self.synopsis_extension)

    def load_preview(self, text):
        body = markdown.markdown(text, extensions=["markdown.extensions.extra"])
        qurl = QUrl.fromLocalFile(filepath_relative(self, "html"))

        self.qwebviewPreview.load(qurl, body=body, scroll_to_bottom=True)

    def load(self):
        try:
            with open(self.path_synopsis(), "r") as iput:
                text = iput.read()

                self.update_scroll()
                self.load_preview(text)
                self.qplaintexteditSynopsis.setPlainText(text)

        except IOError as error:
            if error.errno == 2:
                self.qplaintexteditSynopsis.clear()
            else:
                raise

    def state_save(self):
        from calibre.gui2.viewer.qmainwindow.qmainwindowEbook import vprefs

        vprefs.set('synopsis_mode', self.stackedWidget.currentIndex())

    def state_restore(self):
        from calibre.gui2.viewer.qmainwindow.qmainwindowEbook import vprefs

        mode = vprefs.get('synopsis_mode', None)
        if mode is not None:
            self.stackedWidget.setCurrentIndex(int(mode))
