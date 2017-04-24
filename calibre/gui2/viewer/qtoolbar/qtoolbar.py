from PyQt5.QtWidgets import QToolBar

from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class Qtoolbar(QToolBar, Qwidget):
    def __init__(self, parent=None):
        super(Qtoolbar, self).__init__(parent)

    @property
    def mode_toggle(self):
        return True

