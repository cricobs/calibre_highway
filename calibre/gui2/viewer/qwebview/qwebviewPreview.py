from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtCore import pyqtProperty
from PyQt5.QtCore import pyqtSignal

from calibre.gui2.viewer.qwebpage.qwebpagePreview import QwebpagePreview
from calibre.gui2.viewer.qwebview.qwebview import Qwebview


class QwebviewPreview(Qwebview):
    toPosition = pyqtSignal(str)
    showEditor = pyqtSignal(bool)
    loading = pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super(QwebviewPreview, self).__init__(*args, **kwargs)
        self._body = None

        self.setPage(QwebpagePreview(self))

    def keyPressEvent(self, qkeyevent):
        super(QwebviewPreview, self).keyPressEvent(qkeyevent)
        if qkeyevent.key() in [Qt.Key_Escape, Qt.Key_Return]:
            self.showEditor.emit(True)

    def load(self, qurl, body=None):
        super(QwebviewPreview, self).load(qurl)
        self._body = body

    @pyqtProperty(str)
    def body(self):
        return self._body

    @pyqtSlot()
    def show_editor(self):
        self.showEditor.emit(True)

    @pyqtSlot(str)
    def to_position(self, position):
        self.toPosition.emit(position)
