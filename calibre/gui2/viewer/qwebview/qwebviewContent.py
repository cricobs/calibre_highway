from PyQt5.QtCore import QUrl, pyqtSlot
from PyQt5.QtCore import pyqtProperty
from PyQt5.QtCore import pyqtSignal

from calibre.gui2.viewer.qwebpage.qwebpageContent import QwebpageContent
from calibre.gui2.viewer.qwebview.qwebview import Qwebview
from calibre.library.filepath import filepath_relative


class QwebviewContent(Qwebview):
    contentClick = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(QwebviewContent, self).__init__(*args, **kwargs)

        self._body = None

        self.setPage(QwebpageContent(self))

    @property
    def is_search_replace(self):
        return True

    @pyqtSlot(str)
    def content_click(self, content):
        self.contentClick.emit(content)

    def set_body(self, body):
        self._body = body
        self.load(QUrl.fromLocalFile(filepath_relative(self, "html")))

    @pyqtProperty(str)
    def body(self):
        return self._body
