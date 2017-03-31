from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtWidgets import QWidget

from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class Qdockwidget(QDockWidget, Qwidget):
    def __init__(self, *args, **kwargs):
        super(Qdockwidget, self).__init__(*args, **kwargs)

        self.setTitleBarWidget(self.qwidgettitlebar)
        self.setVisible(self.start_visible)

    @property
    def start_visible(self):
        return False

    @property
    def qwidgettitlebar(self):
        return QWidget()

    def setVisible(self, visible):
        super(Qdockwidget, self).setVisible(visible)

        if visible:
            self.raise_()
