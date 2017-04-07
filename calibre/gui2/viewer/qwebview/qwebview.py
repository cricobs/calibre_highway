from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWebKitWidgets import QWebView, QWebPage

from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class Qwebview(QWebView, Qwidget):
    pageChange = pyqtSignal(QWebPage)

    def __init__(self, *args, **kwargs):
        super(Qwebview, self).__init__(*args, **kwargs)

    def on_qapplication_search(self, qwidget, search):
        if qwidget is not self:
            return

        self.findText(search)

    def setPage(self, qwebpage):
        super(Qwebview, self).setPage(qwebpage)
        self.pageChange.emit(qwebpage)
