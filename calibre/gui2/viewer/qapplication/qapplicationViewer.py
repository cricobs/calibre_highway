from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

from calibre.gui2.viewer.qapplication.qapplication import Qapplication
from calibre.gui2.viewer.qwidget.qwidgetSearchReplace import QwidgetSearchReplace


class QapplicationViewer(Qapplication):
    search = pyqtSignal(QWidget, str)
    replace = pyqtSignal(QWidget, str, str)

    def __init__(self, *args, **kwargs):
        super(QapplicationViewer, self).__init__(*args, **kwargs)

        self.qwidgetSearchReplace = QwidgetSearchReplace()
