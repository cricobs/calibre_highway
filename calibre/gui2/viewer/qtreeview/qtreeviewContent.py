from __future__ import (unicode_literals, division, absolute_import, print_function)

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtWidgets import QToolTip

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
        self.selected_index = None

        self.delegate = Delegate(self)
        self.setItemDelegate(self.delegate)

    @property
    def selected_text(self):
        try:
            return self.selected_index.data()
        except AttributeError:
            pass

    def contextMenuEvent(self, qevent):
        pos = qevent.pos()
        self.selected_index = self.indexAt(pos)

        self.setCurrentIndex(self.selected_index)
        self.setFocus(Qt.OtherFocusReason)

        m = Qmenu(self)
        m.addActions(self.actions())
        m.exec_(self.mapToGlobal(pos))

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
        QApplication.clipboard().setText(getattr(m, 'as_plain_text', ''))
