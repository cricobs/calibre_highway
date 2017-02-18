from PyQt5.QtCore import pyqtProperty, pyqtSlot
from PyQt5.QtCore import pyqtSignal

from calibre.gui2.viewer.qwebview.qwebview import Qwebview


class QwebviewPreview(Qwebview):
    goToPosition = pyqtSignal(str)
    goToBottom = pyqtSignal()
    showEditor = pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super(QwebviewPreview, self).__init__(*args, **kwargs)
        self._body = None
        self._scroll_to_bottom = False

        self.page().setLinkDelegationPolicy(self.page().DelegateAllLinks)
        self.page().settings().setAttribute(self.page().settings().DeveloperExtrasEnabled, True)
        self.page().mainFrame().javaScriptWindowObjectCleared.connect(
            self.on_mainFrame_javaScriptWindowObjectCleared
        )

    @pyqtSlot()
    def load_finished(self):
        if self._scroll_to_bottom:
            # self.scroll_to_bottom()
            self.goToBottom.emit()

    def scroll_to_bottom(self):
        self.page().mainFrame().evaluateJavaScript(
            "window.scrollTo(0, document.body.scrollHeight);")

    def on_mainFrame_javaScriptWindowObjectCleared(self):
        self.page().mainFrame().addToJavaScriptWindowObject("qwebview", self)

    def load(self, qurl, body=None, scroll_to_bottom=False):
        self._body = body
        self._scroll_to_bottom = scroll_to_bottom

        super(QwebviewPreview, self).load(qurl)

    @pyqtSlot(str)
    def goto_position(self, position):
        self.goToPosition.emit(position)

    @pyqtSlot()
    def show_editor(self):
        self.showEditor.emit(True)

    @pyqtProperty(str)
    def body(self):
        return self._body
