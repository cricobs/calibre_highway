from calibre.gui2.main_window import MainWindow
from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class Qmainwindow(MainWindow, Qwidget):
    def __init__(self, *args, **kwargs):
        MainWindow.__init__(self, *args, **kwargs)
        Qwidget.__init__(self, *args, **kwargs)