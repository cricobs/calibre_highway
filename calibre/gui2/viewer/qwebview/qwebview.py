from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWebKitWidgets import QWebView, QWebPage

from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class Qwebview(QWebView, Qwidget):
    pageChange = pyqtSignal(QWebPage)

    def __init__(self, *args, **kwargs):
        super(Qwebview, self).__init__(*args, **kwargs)

    def setPage(self, qwebpage):
        super(Qwebview, self).setPage(qwebpage)
        self.pageChange.emit(qwebpage)

