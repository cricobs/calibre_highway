from PyQt5.QtCore import QObject
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QTreeView

from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class pyqtsignalCallable(QObject):
    pyqtsignal = pyqtSignal()

    def __init__(self, name):
        super(pyqtsignalCallable, self).__init__()
        self.name = name
        self.instance = None
        self.owner = None

    def __getattr__(self, p_str):
        try:
            return getattr(super(pyqtsignalCallable, self), p_str)
        except AttributeError:
            return getattr(self.pyqtsignal, p_str)

    def __get__(self, instance, owner):
        self.instance = instance
        self.owner = owner

        return self

    def __call__(self, *args, **kwargs):
        method = getattr(super(self.owner, self.instance), self.name)
        method(*args, **kwargs)

        self.pyqtsignal.emit()


class Qtreeview(QTreeView, Qwidget):
    selectionChanged = pyqtsignalCallable("selectionChanged")

    def __init__(self, *args, **kwargs):
        super(Qtreeview, self).__init__(*args, **kwargs)

        self.setFocusPolicy(Qt.StrongFocus)

    @property
    def mode_selection(self):
        return True

    @property
    def selected_text(self):
        try:
            return self.currentIndex().data(Qt.DisplayRole)
        except AttributeError:
            pass

    def setCurrentIndex(self, qmodelindex):
        super(Qtreeview, self).setCurrentIndex(qmodelindex)

        if qmodelindex.isValid():
            self.setFocus(Qt.OtherFocusReason)
        else:
            self.clearFocus()

        self.selectionChanged.emit()

    def contextMenuEvent(self, qcontextmenuevent):
        super(Qtreeview, self).contextMenuEvent(qcontextmenuevent)

        self.setCurrentIndex(self.indexAt(qcontextmenuevent.pos()))
