from PyQt5.QtWebKitWidgets import QWebInspector

from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class Qwebinspector(QWebInspector, Qwidget):
    def __init__(self, *args, **kwargs):
        super(Qwebinspector, self).__init__(*args, **kwargs)
