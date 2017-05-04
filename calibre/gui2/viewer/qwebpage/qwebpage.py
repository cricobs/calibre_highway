from PyQt5.QtWebKitWidgets import QWebPage

from calibre.gui2.viewer.qmenu.qmenu import Qmenu
from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class Qwebpage(QWebPage, Qwidget):
    def __init__(self, *args, **kwargs):
        super(Qwebpage, self).__init__(*args, **kwargs)

        self.mainFrame().javaScriptWindowObjectCleared.connect(
            self.on_mainFrame_javaScriptWindowObjectCleared
        )

    @property
    def mode_selection(self):
        return True

    def on_mainFrame_javaScriptWindowObjectCleared(self):
        self.mainFrame().addToJavaScriptWindowObject("qwebview", self.view())

    def goto_hash(self, hash):
        self.mainFrame().evaluateJavaScript("window.location.hash = '" + hash + "';")

    def createStandardContextMenu(self):
        return Qmenu(self.view())
