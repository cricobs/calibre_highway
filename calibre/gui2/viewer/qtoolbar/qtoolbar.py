from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QToolBar

from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class Qtoolbar(QToolBar, Qwidget):
    def __init__(self, parent=None):
        super(Qtoolbar, self).__init__(parent)

        self.setFocusPolicy(Qt.NoFocus)

    @property
    def mode_global_qaction(self):
        return True

    def _addAction(self, action):
        super(Qtoolbar, self)._addAction(action)
        if action.menu():
            data = action.data() or {}
            popup = data.get("popup", None)
            if popup is not None:
                qwidget = self.widgetForAction(action)
                qwidget.setPopupMode(getattr(qwidget, popup))

    @property
    def mode_toggle(self):
        return True

    def addAction(self, action):
        self._addAction(action)
