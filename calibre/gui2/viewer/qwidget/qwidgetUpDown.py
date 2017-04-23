from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QToolButton

from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class QwidgetUpDown(Qwidget):
    clicked = pyqtSignal(QToolButton)

    def __init__(self, *args, **kwargs):
        super(QwidgetUpDown, self).__init__(*args, **kwargs)

        s = self.style()
        h = self.height() / 2

        self.qtoolbuttonUp.setIcon(s.standardIcon(s.SP_ArrowUp))
        self.qtoolbuttonUp.setMaximumHeight(h)

        self.qtoolbuttonDown.setIcon(s.standardIcon(s.SP_ArrowDown))
        self.qtoolbuttonDown.setMaximumHeight(h)

        self.setContentsMargins(2, 2, 2, 2)

    @pyqtSlot(bool)
    def on_qtoolbuttonDown_clicked(self, checked):
        self.clicked.emit(self.sender())

    @pyqtSlot(bool)
    def on_qtoolbuttonUp_clicked(self, checked):
        self.clicked.emit(self.sender())
