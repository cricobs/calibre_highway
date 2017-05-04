from __future__ import (unicode_literals, division, absolute_import, print_function)

from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtWidgets import QToolTip

from calibre.gui2 import error_dialog
from calibre.gui2.viewer.qmenu.qmenu import Qmenu
from calibre.gui2.viewer.qtreeview.qtreeview import Qtreeview

_ = _


class Delegate(QStyledItemDelegate):
    def helpEvent(self, ev, view, option, index):
        # Show a tooltip only if the item is truncated
        if not ev or not view:
            return False
        if ev.type() == ev.ToolTip:
            rect = view.visualRect(index)
            size = self.sizeHint(option, index)
            if rect.width() < size.width():
                tooltip = index.data(Qt.DisplayRole)
                QToolTip.showText(ev.globalPos(), tooltip, view)
                return True
        return QStyledItemDelegate.helpEvent(self, ev, view, option, index)


class QtreeviewContent(Qtreeview):
    searched = pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super(QtreeviewContent, self).__init__(*args, **kwargs)

        self.delegate = Delegate(self)
        self.setItemDelegate(self.delegate)

    def search(self, search, backwards=False):
        # fixme use direction
        index = self.model().search(search)
        if index.isValid():
            self.searched.emit(index)
        else:
            error_dialog(
                self, 'No matches found',
                'There are no Table of Contents entries matching: ' + search, show=True)

    def set_current_entry(self):
        entry = self.model().currently_viewed_entry
        if not entry:
            return

        self.scrollTo(entry.index(), self.PositionAtTop)
        self.setCurrentIndex(entry.index())

    def contextMenuEvent(self, qevent):
        super(QtreeviewContent, self).contextMenuEvent(qevent)

        m = Qmenu(self)
        m.addActions(self.actions())
        m.exec_(self.mapToGlobal(qevent.pos()))

    def mouseMoveEvent(self, ev):
        if self.indexAt(ev.pos()).isValid():
            self.setCursor(Qt.PointingHandCursor)
        else:
            self.unsetCursor()

        return super(QtreeviewContent, self).mouseMoveEvent(ev)

    def expand_tree(self, index=None):
        index = index if index else self.selected_index
        self.expand(index)
        i = -1
        while True:
            i += 1
            child = index.child(i, 0)
            if not child.isValid():
                break
            self.expand_tree(child)

    def copy_to_clipboard(self):
        m = self.model()
        self.qapplication.copy_text(getattr(m, 'as_plain_text', ''))

    def showEvent(self, qshowevent):
        super(QtreeviewContent, self).showEvent(qshowevent)

        self.set_current_entry()

    def hideEvent(self, qhideevent):
        super(QtreeviewContent, self).hideEvent(qhideevent)

        self.setCurrentIndex(QModelIndex())  # hint clear selection
