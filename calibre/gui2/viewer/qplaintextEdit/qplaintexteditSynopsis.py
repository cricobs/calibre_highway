from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QTextCursor

from calibre.gui2.viewer.qplaintextEdit.qplaintextedit import Qplaintextedit


class QplaintexteditSynopsis(Qplaintextedit):
    contentChanged = pyqtSignal()
    showPreview = pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super(QplaintexteditSynopsis, self).__init__(*args, **kwargs)

    def setPlainText(self, p_str):
        super(QplaintexteditSynopsis, self).setPlainText(p_str)

        self.contentChanged.emit()

    def scroll_to_bottom(self):
        self.moveCursor(QTextCursor.End)
        self.ensureCursorVisible()

    def keyPressEvent(self, qkeyevent):
        super(QplaintexteditSynopsis, self).keyPressEvent(qkeyevent)
        if qkeyevent.key() == Qt.Key_Escape:
            self.showPreview.emit(True)
