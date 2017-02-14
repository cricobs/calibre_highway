from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtProperty, pyqtSlot
from PyQt5.QtCore import pyqtSignal

from calibre.gui2.viewer.qwebview.qwebview import Qwebview


class QwebviewPreview(Qwebview):
    goToPosition = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(QwebviewPreview, self).__init__(*args, **kwargs)
        self._body = None

        self.page().setLinkDelegationPolicy(self.page().DelegateAllLinks)
        self.page().settings().setAttribute(self.page().settings().DeveloperExtrasEnabled, True)
        self.page().mainFrame().javaScriptWindowObjectCleared.connect(
            self.on_mainFrame_javaScriptWindowObjectCleared
        )

    def on_mainFrame_javaScriptWindowObjectCleared(self):
        self.page().mainFrame().addToJavaScriptWindowObject("qwebview", self)

    def load(self, qurl, body=None):
        self._body = body

        super(QwebviewPreview, self).load(qurl)

    @pyqtSlot(str)
    def goto_position(self, position):
        self.goToPosition.emit(position)

    @pyqtProperty(str)
    def body(self):
        return self._body
