from __future__ import (unicode_literals, division, absolute_import, print_function)

from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtWidgets import QToolTip

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

        self.customContextMenuRequested.connect(self.context_menu)

    @property
    def mode_search(self):
        return self.SEARCH

    def mouseMoveEvent(self, ev):
        if self.indexAt(ev.pos()).isValid():
            self.setCursor(Qt.PointingHandCursor)
        else:
            self.unsetCursor()

        return super(QtreeviewContent, self).mouseMoveEvent(ev)

    def expand_tree(self, index):
        self.expand(index)
        i = -1
        while True:
            i += 1
            child = index.child(i, 0)
            if not child.isValid():
                break
            self.expand_tree(child)

    def context_menu(self, pos):
        index = self.indexAt(pos)
        m = QMenu(self)
        if index.isValid():
            m.addAction(_('Expand all items under %s') % index.data(), partial(self.expand_tree, index))
        m.addSeparator()
        m.addAction(_('Expand all items'), self.expandAll)
        m.addAction(_('Collapse all items'), self.collapseAll)
        m.addSeparator()
        m.addAction(_('Copy table of contents to clipboard'), self.copy_to_clipboard)
        m.exec_(self.mapToGlobal(pos))

    def keyPressEvent(self, event):
        try:
            if self.handle_shortcuts(event):
                return
        except AttributeError:
            pass

        super(QtreeviewContent, self).keyPressEvent(event)

    def copy_to_clipboard(self):
        m = self.model()
        QApplication.clipboard().setText(getattr(m, 'as_plain_text', ''))
