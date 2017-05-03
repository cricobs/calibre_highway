from PyQt5.QtCore import QRegExp
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal

from calibre.gui2.viewer.qobject.qobjectScrollPosition import QobjectScrollPosition
from calibre.gui2.viewer.qplaintextedit.qplaintextedit import Qplaintextedit
from calibre.gui2.viewer.qsyntaxhighlighter.qsyntaxhighlighterSynopsis import \
    QsyntaxhighlighterSynopsis


class QplaintexteditEdit(Qplaintextedit):
    showPreview = pyqtSignal(bool)
    positionSave = pyqtSignal()
    positionLoad = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(QplaintexteditEdit, self).__init__(*args, **kwargs)

        QobjectScrollPosition(self)

        self.qsyntaxhiglighter = QsyntaxhighlighterSynopsis(self.document())

    def on_qaction_triggered(self):
        c = self.textCursor()
        self.insert_format(c, c.selectedText(), **self.sender().data())
        self.setFocus(Qt.OtherFocusReason)

    @property
    def selected_text(self):
        return self.textCursor().selectedText()

    def contextMenuEvent(self, qevent):
        menu = self.qmenu_format
        if not menu.exec_(qevent.globalPos()):
            super(QplaintexteditEdit, self).contextMenuEvent(qevent)

    def replace(self, search, replace, backwards=False):
        self.search(search)
        t = self.textCursor()
        if t.hasSelection():
            t.insertText(replace)

    def search(self, search, backwards=False):
        self.setReadOnly(True)  # agtft QlineditSearchReplace return pressed is propagated

        qregexp = QRegExp(search)
        qtextcursor = self.document().find(qregexp, self.textCursor().position())

        if not qtextcursor.isNull():
            self.setTextCursor(qtextcursor)

        QTimer.singleShot(0, lambda: self.setReadOnly(False))

    @property
    def mode_search(self):
        return self.SEARCH | self.REPLACE

    def insert_format(self, cursor, text, newline=False, position=True, start=None, end=None, **kwargs):
        cursor.beginEditBlock()
        if newline and not cursor.atBlockStart():
            cursor.insertText('\n')
        if start:
            cursor.insertText(start)
        if text:
            cursor.insertText(text)
        if position:
            cursor.setPosition(cursor.position())
            self.setTextCursor(cursor)
        if end:
            cursor.insertText(end)
        cursor.endEditBlock()

    def setPlainText(self, p_str):
        self.positionSave.emit()
        super(QplaintexteditEdit, self).setPlainText(p_str)
        self.positionLoad.emit()

    def keyPressEvent(self, qkeyevent):
        super(QplaintexteditEdit, self).keyPressEvent(qkeyevent)
        if qkeyevent.key() == Qt.Key_Escape:
            self.showPreview.emit(True)
