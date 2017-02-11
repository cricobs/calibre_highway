from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal

from calibre.gui2.viewer.qlistwidget.qlistwidget import Qlistwidget


class QlistwidgetBookmark(Qlistwidget):
    changed = pyqtSignal()
    bookmark_activated = pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super(QlistwidgetBookmark, self).__init__(*args, **kwargs)

        self.viewport().setAcceptDrops(True)
        self.setDropIndicatorShown(True)

    def dropEvent(self, ev):
        super(QlistwidgetBookmark, self).dropEvent(ev)

        if ev.isAccepted():
            self.changed.emit()

    def keyPressEvent(self, ev):
        if ev.key() in (Qt.Key_Enter, Qt.Key_Return):
            i = self.currentItem()
            if i is not None:
                self.bookmark_activated.emit(i)
                ev.accept()
                return

        if ev.key() in (Qt.Key_Delete, Qt.Key_Backspace):
            i = self.currentItem()
            if i is not None:
                self.ac_delete.trigger()
                ev.accept()
                return

        return super(QlistwidgetBookmark, self).keyPressEvent(ev)
