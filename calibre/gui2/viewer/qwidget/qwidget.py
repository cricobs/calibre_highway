from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

from calibre.gui2.viewer.qaction.qaction import Qaction
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

        if self.mode_toggle:
            self.qaction_toggle = Qaction(self)
            self.qaction_toggle.triggered.connect(self.setVisible)
            self.qaction_toggle.triggered.connect(self.on_qaction_toggle_triggered)

            q = getattr(self, "toggleViewAction", None)
            if q:
                self.qaction_toggle.setText(q().text())

    def setWindowTitle(self, p_str):
        super(Qwidget, self).setWindowTitle(p_str)

        if self.mode_toggle:
            try:
                self.qaction_toggle.setText(p_str)
            except AttributeError:
                pass

    @property
    def mode_toggle(self):
        return False

    def on_qaction_toggle_triggered(self, checked):
        """
        calle if getattr(self, "toggleViewAction")
        :param checked:
        :return:
        """
        pass

    def on_qapplication_aboutToQuit(self):
        """
        called if self.mode_save
        :return:
        """
        pass

    def search(self, search, backwards=False):
        """
        called on_qapplication_search
        :param search:
        :param backwards:
        :return:
        """
        pass

    def replace(self, search, replace, backwards=False):
        """
        called on on_qapplication_replace
        :param search:
        :param replace:
        :param backwards:
        :return:
        """
        pass

    def on_qapplication_search(self, qwidget, search, backwards):
        """
        called if mode_search ^ self.NONE
        :param qwidget:
        :param search:
        :param backwards:
        :return:
        """
        if qwidget is self:
            self.search(search, backwards)

    def on_qapplication_replace(self, qwidget, search, replace, backwards):
        """
        called if mode_search ^ self.NONE
        :param qwidget:
        :param search:
        :param replace:
        :param backwards:
        :return:
        """
        if qwidget is self:
            self.replace(search, replace, backwards)

    @property
    def mode_save(self):
        """
        connect on_qapplication_aboutToQuit
        :return:
        """
        return False

    @property
    def mode_visibility(self):
        """
        emit visibilityChanged
        :return:
        """
        return False

    @property
    def mode_search(self):
        """
        connect on_qapplication_replace, on_qapplication_search
        :return:
        """
        return self.NONE

    def visibility_changed(self, visibility):
        if self.mode_visibility:
            self.visibilityChanged.emit(visibility)

        if self.mode_toggle:
            self.qaction_toggle.setChecked(visibility)

    def hideEvent(self, qhideevent):
        super(Qwidget, self).hideEvent(qhideevent)

        self.visibility_changed(False)

    def showEvent(self, qshowevent):
        super(Qwidget, self).showEvent(qshowevent)

        self.visibility_changed(True)
