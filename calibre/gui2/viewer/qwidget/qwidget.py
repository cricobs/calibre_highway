from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

from calibre.gui2.viewer.qobject.qobject import Qobject


class Qwidget(QWidget, Qobject):
    visibilityChanged = pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super(Qwidget, self).__init__(*args, **kwargs)

    @property
    def is_visibility_tracked(self):
        return False

    @property
    def is_search_replace(self):
        return False

    def hideEvent(self, qhideevent):
        super(Qwidget, self).hideEvent(qhideevent)

        if self.is_visibility_tracked:
            self.visibilityChanged.emit(False)

    def showEvent(self, qshowevent):
        super(Qwidget, self).showEvent(qshowevent)
        if self.is_visibility_tracked:
            self.visibilityChanged.emit(True)
