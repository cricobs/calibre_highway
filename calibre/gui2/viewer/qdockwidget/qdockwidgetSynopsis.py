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
        self.toolButtonReload.setIcon(QIcon(I("view-refresh.png")))

        self.qwebviewPreview.page().mainFrame().contentsSizeChanged.connect(
            self.on_mainFrame_contentSizeChanged)

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
        self.qwebviewPreview.load(
            QUrl.fromLocalFile(filepath_relative(self, "html")),
            markdown.markdown(text, extensions=["markdown.extensions.extra"])
        )

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
