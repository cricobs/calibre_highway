from PyQt5.QtWebKitWidgets import QWebView

from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class Qwebview(QWebView, Qwidget):
    def __init__(self, *args, **kwargs):
        super(Qwebview, self).__init__(*args, **kwargs)
