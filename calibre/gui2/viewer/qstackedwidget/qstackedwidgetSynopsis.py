from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from calibre.gui2.viewer.qdialog.qdialogConfig import config
from calibre.gui2.viewer.qobject.qobjectScrollSynchronize import QobjectScrollSynchronize
from calibre.gui2.viewer.qstackedwidget.qstackedwidget import Qstackedwidget
from calibre.library.filepath import filepath_relative

I = I


# todo 1
# - editor replace
# - editor shortcuts
# - store within .epub file
# - track with git
# - editor format text
# - spell check

# todo 2
# - use qtoolbutton + qmenu for markdown format
# - save and load position in relation to book
# - showEdit signal not being sent when double clicking on new preview body
# - scroll synchronize not working on startup from qplaintexteditEdit

# todo 3
# - use QtabwidgetSynopsis instead of QstackedwidgetSynopsis

class QstackedwidgetSynopsis(Qstackedwidget):
    def __init__(self, *args, **kwargs):
        super(QstackedwidgetSynopsis, self).__init__(*args, **kwargs)

        self.path_source = None

        # config
        self.synopsis_extension = None
        self.mono_family = None
        self.default_font_size = None
        self.synopsis_size = None

        self.update_config()

        self.toolButtonRedo.setIcon(QIcon(I("edit-redo.png")))
        self.toolButtonUndo.setIcon(QIcon(I("edit-undo.png")))
        self.toolButtonSave.setIcon(QIcon(I("save.png")))
        self.toolButtonPreview.setIcon(QIcon(I("beautify.png")))
        self.toolButtonReload.setIcon(QIcon(I("view-refresh.png")))

        self.qcomboboxMarkdown.addItems(sorted(self.qplaintexteditSynopsis.formats.keys()))

        self.qobjectscrollsynchronize = QobjectScrollSynchronize(
            self.qwebviewPreview, self.qplaintexteditSynopsis)

        QApplication.instance().aboutToQuit.connect(self.on_qapplication_aboutToQuit)

        self.state_restore()

    def preview(self):
        self.save()
        self.qobjectscrollsynchronize.reload()
        self.setCurrentIndex(1)

    def edit(self):
        self.qobjectscrollsynchronize.reload()
        self.setCurrentIndex(0)
        self.qplaintexteditSynopsis.setFocus()

    def update_config(self):
        opts = config().parse()
        self.synopsis_extension = opts.synopsis_extension
        self.mono_family = opts.mono_family
        self.default_font_size = opts.default_font_size
        self.synopsis_size = opts.synopsis_size

        self.qplaintexteditSynopsis.setFont(QFont(self.mono_family))

    def append(self, text, position=None):
        self.qplaintexteditSynopsis.appendPlainText(text)

        if self.currentIndex():
            if position:
                self.qwebviewPreview.scroll_to_position(position)

            self.save()

    def save(self):
        try:
            with open(self.path_synopsis(), "r+") as oput:
                self.save_file(oput)
        except IOError as error:
            if error.errno != 2:
                raise

            if not self.qplaintexteditSynopsis.toPlainText():
                return

            with open(self.path_synopsis(), "ab+") as oput:
                self.save_file(oput)

    def save_file(self, oput):
        text = self.qplaintexteditSynopsis.toPlainText()
        if text == oput.read():
            return

        oput.seek(0)
        oput.write(text)
        oput.truncate()

        self.qwebviewPreview.set_body(text)
        self.qplaintexteditSynopsis.document().setModified(False)

    def path_synopsis(self):
        self.update_config()
        if not self.synopsis_extension:
            raise ValueError("synopsis extension unset")

        return filepath_relative(self.path_source, extension=self.synopsis_extension)

    def reload(self):
        if self.path_source:
            self.load(self.path_source)

    def load(self, path):
        if self.path_source:
            self.save()

        self.path_source = path
        try:
            with open(self.path_synopsis(), "r") as iput:
                text = iput.read()

                self.qwebviewPreview.set_body(text)
                self.qplaintexteditSynopsis.setPlainText(text)

        except IOError as error:
            if error.errno == 2:
                self.qplaintexteditSynopsis.clear()
            else:
                raise

    def state_save(self):
        from calibre.gui2.viewer.qmainwindow.qmainwindowEbook import vprefs

        vprefs.set('synopsis_mode', self.currentIndex())

    def state_restore(self):
        from calibre.gui2.viewer.qmainwindow.qmainwindowEbook import vprefs

        self.setCurrentIndex(int(vprefs.get('synopsis_mode', None) or 0))

    @pyqtSlot(str)
    def on_qwebviewContent_contentClick(self, hash):
        self.qwebviewPreview.goto_hash(hash)
        self.setCurrentIndex(self.indexOf(self.qwebviewPreview.parent()))

    @pyqtSlot(str)
    def on_qwebviewPreview_contentChange(self, content):
        self.qwebviewContent.set_body(content)

    @pyqtSlot(str)
    def on_qcomboboxMarkdown_activated(self, text):
        self.qplaintexteditSynopsis.insertFormat(text)
        self.qcomboboxMarkdown.setCurrentIndex(0)

    @pyqtSlot(bool)
    def on_toolButtonPreview_clicked(self, checked):
        self.preview()

    @pyqtSlot(bool)
    def on_qwebviewPreview_showEditor(self):
        self.edit()

    @pyqtSlot(bool)
    def on_qplaintexteditSynopsis_showPreview(self):
        self.preview()

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
        self.reload()

    @pyqtSlot(bool)
    def on_toolButtonSave_clicked(self, checked):
        self.save()

    def on_qapplication_aboutToQuit(self):
        self.save()
        self.state_save()
