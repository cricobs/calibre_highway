from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStackedWidget

from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class Qstackedwidget(QStackedWidget, Qwidget):
    def __init__(self, *args, **kwargs):
        super(Qstackedwidget, self).__init__(*args, **kwargs)

    def keyPressEvent(self, event):
        index = None
        if event.key() == Qt.Key_Right:
            index = self.currentIndex() - 1
        elif event.key() == Qt.Key_Left:
            index = self.currentIndex() + 1

        if index is not None:
            self.setCurrentIndex(index)

        super(Qstackedwidget, self).keyPressEvent(event)
