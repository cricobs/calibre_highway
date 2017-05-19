from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QFont

from calibre.gui2.viewer.library.filepath import filepath_relative
from calibre.gui2.viewer.qdialog.qdialogConfig import config
from calibre.gui2.viewer.qobject.qobjectScrollSynchronize import QobjectScrollSynchronize
from calibre.gui2.viewer.qstackedwidget.qstackedwidget import Qstackedwidget

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

        self.qobjectscrollsynchronize = QobjectScrollSynchronize(
            self.qwebviewPreview, self.qplaintexteditEdit)

        self.restore_state()

    @property
    def mode_view(self):
        return True

    def on_topLevelWidget_iteratorChanged(self, ebookiterator):
        self.load(ebookiterator.pathtoebook)

    def preview(self):
        self.save()
        self.qobjectscrollsynchronize.reload()
        self.setCurrentIndex(1)

    def edit(self):
        self.qobjectscrollsynchronize.reload()
        self.setCurrentIndex(0)
        self.qplaintexteditEdit.setFocus()

    def update_config(self):
        opts = config().parse()
        self.synopsis_extension = opts.synopsis_extension
        self.mono_family = opts.mono_family
        self.default_font_size = opts.default_font_size
        self.synopsis_size = opts.synopsis_size

        self.qplaintexteditEdit.setFont(QFont(self.mono_family))

    def save(self):
        try:
            with open(self.path_synopsis(), "r+") as oput:
                self.save_file(oput)
        except IOError as error:
            if error.errno != 2:
                raise

            if not self.qplaintexteditEdit.toPlainText():
                return

            with open(self.path_synopsis(), "ab+") as oput:
                self.save_file(oput)

    def save_file(self, oput):
        text = self.qplaintexteditEdit.toPlainText()
        if text == oput.read():
            return

        oput.seek(0)
        oput.write(text)
        oput.truncate()

        self.qwebviewPreview.set_body(text)
        self.qplaintexteditEdit.document().setModified(False)

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
                self.qplaintexteditEdit.setPlainText(text)

        except IOError as error:
            if error.errno == 2:
                self.qwebviewPreview.clear()
                self.qplaintexteditEdit.clear()
            else:
                raise

    def save_state(self):
        from calibre.gui2.viewer.qmainwindow.qmainwindowViewer import vprefs

        vprefs.set('synopsis_mode', self.currentIndex())

    def restore_state(self):
        from calibre.gui2.viewer.qmainwindow.qmainwindowViewer import vprefs

        self.setCurrentIndex(int(vprefs.get('synopsis_mode', None) or 0))

    @pyqtSlot()
    def on_qplaintexteditEdit_save(self):
        self.save()

    @pyqtSlot(str)
    def on_qplaintexteditEdit_scrollToMarkdownPosition(self, position):
        self.qwebviewPreview.scroll_to_position(position)

    @pyqtSlot(str)
    def on_qwebviewContent_contentClick(self, hash):
        self.qwebviewPreview.goto_hash(hash)
        self.setCurrentIndex(self.indexOf(self.qwebviewPreview.parent()))

    def redo(self):
        self.qplaintexteditEdit.redo()

    def undo(self):
        self.qplaintexteditEdit.undo()

    @pyqtSlot(str)
    def on_qwebviewPreview_contentChange(self, content):
        self.qwebviewContent.set_body(content)

    @pyqtSlot(bool)
    def on_qwebviewPreview_showEditor(self):
        self.edit()

    @pyqtSlot(bool)
    def on_qplaintexteditEdit_modificationChanged(self, changed):
        self.qaction_save.setEnabled(changed)

    @pyqtSlot(bool)
    def on_qplaintexteditEdit_redoAvailable(self, available):
        self.qaction_redo.setEnabled(available)

    @pyqtSlot(bool)
    def on_qplaintexteditEdit_undoAvailable(self, available):
        self.qaction_undo.setEnabled(available)

    def on_qapplication_aboutToQuit(self):
        if self.path_source:
            self.save()

        self.save_state()

    @property
    def mode_save(self):
        return True

    def addAction(self, qaction):
        setattr(self, qaction.objectName(), qaction)

        super(QstackedwidgetSynopsis, self).addAction(qaction)
