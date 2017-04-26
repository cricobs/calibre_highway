from PyQt5.QtCore import QUrl, pyqtSlot
from PyQt5.QtCore import pyqtProperty
from PyQt5.QtCore import pyqtSignal

from calibre.gui2.viewer.library.filepath import filepath_relative
from calibre.gui2.viewer.qwebview.qwebview import Qwebview


class QwebviewContent(Qwebview):
    contentClick = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(QwebviewContent, self).__init__(*args, **kwargs)

        self._body = None

    @property
    def mode_search(self):
        return self.SEARCH

    @pyqtSlot(str)
    def content_click(self, content):
        self.contentClick.emit(content)

    def set_body(self, body):
        self._body = body
        self.load(QUrl.fromLocalFile(filepath_relative(self, "html")))

    @pyqtProperty(str)
    def body(self):
        return self._body
