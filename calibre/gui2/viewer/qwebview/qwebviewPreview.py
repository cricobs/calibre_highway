from PyQt5.QtCore import QUrl
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtCore import pyqtProperty
from PyQt5.QtCore import pyqtSignal

from calibre.ebooks import markdown
from calibre.gui2.viewer.qobject.qobjectScrollPosition import QobjectScrollPosition
from calibre.gui2.viewer.qwebpage.qwebpagePreview import QwebpagePreview
from calibre.gui2.viewer.qwebview.qwebview import Qwebview
from calibre.library.filepath import filepath_relative


class QwebviewPreview(Qwebview):
    showEditor = pyqtSignal(bool)
    positionChange = pyqtSignal(str)
    positionSave = pyqtSignal()
    positionLoad = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(QwebviewPreview, self).__init__(*args, **kwargs)
        self._body = None
        self._position = None

        QobjectScrollPosition(self)

        self.setPage(QwebpagePreview(self))

        self.page().mainFrame().contentsSizeChanged.connect(self.on_mainFrame_contentsSizeChanged)

    def on_mainFrame_contentsSizeChanged(self):
        self.positionLoad.emit()

    def keyPressEvent(self, qkeyevent):
        super(QwebviewPreview, self).keyPressEvent(qkeyevent)
        if qkeyevent.key() in [Qt.Key_Escape, Qt.Key_Return]:
            self.showEditor.emit(True)

    def mouseDoubleClickEvent(self, qmouseevent):
        super(QwebviewPreview, self).mouseDoubleClickEvent(qmouseevent)
        if self._body is None:
            self.showEditor.emit(True)

    def set_body(self, body):
        self._body = markdown.markdown(body, extensions=["markdown.extensions.extra"])

        self.positionSave.emit()
        self.load(QUrl.fromLocalFile(filepath_relative(self, "html")))

    @pyqtProperty(str)
    def body(self):
        return self._body

    @pyqtSlot()
    def show_editor(self):
        self.showEditor.emit(True)

    @pyqtSlot(str)
    def position_change(self, position):
        self.positionChange.emit(position)

    @pyqtProperty(str)
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    def scroll_to_position(self, position):
        self.position = position
