from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

from calibre.gui2.viewer.qobject.qobject import Qobject


class Qwidget(QWidget, Qobject):
    visibilityChanged = pyqtSignal(bool)
    NONE, SEARCH, REPLACE, ALL = list(map(lambda x: 2 ** x, range(4)))

    def __init__(self, *args, **kwargs):
        super(Qwidget, self).__init__(*args, **kwargs)

        if self.mode_search:
            self.qapplication.search.connect(self.on_qapplication_search)
            self.qapplication.replace.connect(self.on_qapplication_replace)

    def search(self, search, backwards=False):
        pass

    def replace(self, search, replace, backwards=False):
        pass

    def on_qapplication_search(self, qwidget, search):
        if qwidget is self:
            self.search(search)

    def on_qapplication_replace(self, qwidget, search, replace):
        if qwidget is self:
            self.replace(search, replace)

    @property
    def is_visibility_tracked(self):
        return False

    @property
    def mode_search(self):
        return self.NONE

    def hideEvent(self, qhideevent):
        super(Qwidget, self).hideEvent(qhideevent)

        if self.is_visibility_tracked:
            self.visibilityChanged.emit(False)

    def showEvent(self, qshowevent):
        super(Qwidget, self).showEvent(qshowevent)
        if self.is_visibility_tracked:
            self.visibilityChanged.emit(True)
