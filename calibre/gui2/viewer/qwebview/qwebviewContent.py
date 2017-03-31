from PyQt5.QtCore import QUrl
from PyQt5.QtCore import pyqtProperty

from calibre.gui2.viewer.qwebpage.qwebpageContent import QwebpageContent
from calibre.gui2.viewer.qwebview.qwebview import Qwebview
from calibre.library.filepath import filepath_relative


class QwebviewContent(Qwebview):
    def __init__(self, *args, **kwargs):
        super(QwebviewContent, self).__init__(*args, **kwargs)

        self._body = None

        self.setPage(QwebpageContent(self))

    def set_body(self, body):
        self._body = body

        self.load(QUrl.fromLocalFile(filepath_relative(self, "html")))

    @pyqtProperty(str)
    def body(self):
        return self._body
