from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

from calibre.gui2.viewer.qobject.qobject import Qobject


class Qwidget(QWidget, Qobject):
    visibilityChanged = pyqtSignal(bool)
    NONE, SEARCH, REPLACE, ALL = list(map(lambda x: 2 ** x, range(4)))

    def __init__(self, *args, **kwargs):
        super(Qwidget, self).__init__(*args, **kwargs)

        if self.mode_search ^ self.NONE:
            self.qapplication.search.connect(self.on_qapplication_search)
            self.qapplication.replace.connect(self.on_qapplication_replace)

        if self.mode_save:
            self.qapplication.aboutToQuit.connect(self.on_qapplication_aboutToQuit)

    def on_qapplication_aboutToQuit(self):
        """
        called if mode_save is True
        :return:
        """
        pass

    def search(self, search, backwards=False):
        pass

    def replace(self, search, replace, backwards=False):
        pass

    def on_qapplication_search(self, qwidget, search):
        """
        called if mode_search ^ self.NONE
        :param qwidget:
        :param search:
        :return:
        """
        if qwidget is self:
            self.search(search)

    def on_qapplication_replace(self, qwidget, search, replace):
        """
        called if mode_search ^ self.NONE
        :param qwidget:
        :param search:
        :param replace:
        :return:
        """
        if qwidget is self:
            self.replace(search, replace)

    @property
    def mode_save(self):
        return False

    @property
    def mode_visibility(self):
        return False

    @property
    def mode_search(self):
        return self.NONE

    def hideEvent(self, qhideevent):
        super(Qwidget, self).hideEvent(qhideevent)

        if self.mode_visibility:
            self.visibilityChanged.emit(False)

    def showEvent(self, qshowevent):
        super(Qwidget, self).showEvent(qshowevent)
        if self.mode_visibility:
            self.visibilityChanged.emit(True)
