import json

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal

from calibre.gui2.viewer.qobject.qobjectScrollPosition import QobjectScrollPosition
from calibre.gui2.viewer.qplaintextedit.qplaintextedit import Qplaintextedit
from calibre.gui2.viewer.qsyntaxhighlighter.qsyntaxhighlighterSynopsis import \
    QsyntaxhighlighterSynopsis
from calibre.library.filepath import filepath_relative


class QplaintexteditEdit(Qplaintextedit):
    showPreview = pyqtSignal(bool)
    positionSave = pyqtSignal()
    positionLoad = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(QplaintexteditEdit, self).__init__(*args, **kwargs)

        QobjectScrollPosition(self)

        # self.dict = enchant.Dict()

        self.qsyntaxhiglighter = QsyntaxhighlighterSynopsis(self.document())
        # self.qsyntaxhiglighter.setDict(self.dict)

        with open(filepath_relative(self, "json")) as iput:
            self.formats = json.load(iput)["formats"]
    @property
    def is_search_replace(self):
        return True

    def insertFormat(self, format):
        c = self.textCursor()
        self._insertFormat(c, c.selectedText(), **self.formats.get(format, None))
        self.setFocus(Qt.OtherFocusReason)

    def _insertFormat(self, cursor, text, newline=False, position=True, start=None, end=None):
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
