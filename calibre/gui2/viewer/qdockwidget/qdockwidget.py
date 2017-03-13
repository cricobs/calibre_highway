from PyQt5.QtWidgets import QDockWidget

from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class Qdockwidget(QDockWidget, Qwidget):
    def __init__(self, *args, **kwargs):
        super(Qdockwidget, self).__init__(*args, **kwargs)

        self.close()
        self.toggleviewaction = self.toggleViewAction()

    def setVisible(self, bool):
        super(Qdockwidget, self).setVisible(bool)

        if bool:
            self.raise_()

