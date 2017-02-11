import time
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QApplication

from calibre.gui2.viewer.qlineedit.qlineedit import Qlineedit

_ = _
I = I


class QlineeditSearch(Qlineedit):
    key_pressed = pyqtSignal(object)
    select_on_mouse_press = None

    def keyPressEvent(self, event):
        self.key_pressed.emit(event)

        super(QlineeditSearch, self).keyPressEvent(event)

    def dropEvent(self, ev):
        self.parent().normalize_state()

        return super(QlineeditSearch, self).dropEvent(ev)

    def contextMenuEvent(self, ev):
        self.parent().normalize_state()
        menu = self.createStandardContextMenu()
        menu.setAttribute(Qt.WA_DeleteOnClose)
        for action in menu.actions():
            if action.text().startswith(_('&Paste') + '\t'):
                break
        ac = menu.addAction(_('Paste and &search'))
        ac.setEnabled(bool(QApplication.clipboard().text()))
        ac.setIcon(QIcon(I('search.png')))
        ac.triggered.connect(self.paste_and_search)
        menu.insertAction(action, ac)
        menu.exec_(ev.globalPos())

    def paste_and_search(self):
        self.paste()
        ev = QKeyEvent(QKeyEvent.KeyPress, Qt.Key_Enter, Qt.NoModifier)
        self.keyPressEvent(ev)

    @pyqtSlot()
    def paste(self, *args):
        self.parent().normalize_state()

        return super(QlineeditSearch, self).paste()

    def focusInEvent(self, ev):
        self.select_on_mouse_press = time.time()

        return super(QlineeditSearch, self).focusInEvent(ev)

    def mousePressEvent(self, ev):
        super(QlineeditSearch, self).mousePressEvent(ev)

        if self.select_on_mouse_press is not None and abs(time.time() - self.select_on_mouse_press) < 0.2:
            self.selectAll()
        self.select_on_mouse_press = None
