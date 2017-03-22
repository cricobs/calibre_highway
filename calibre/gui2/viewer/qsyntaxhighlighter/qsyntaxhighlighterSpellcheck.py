import re

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCharFormat

from calibre.gui2.viewer.qsyntaxhighlighter.qsyntaxhighlighter import Qsyntaxhighlighter


class QsyntaxhighlighterSpellcheck(Qsyntaxhighlighter):
    WORDS = u'(?iu)[\w\']+'

    def __init__(self, *args, **kwargs):
        super(QsyntaxhighlighterSpellcheck, self).__init__(*args, **kwargs)
        self.dict = None

    def setDict(self, dict):
        self.dict = dict

    def highlightBlock(self, text):
        if not self.dict:
            return

        text = unicode(text)

        format = QTextCharFormat()
        format.setUnderlineColor(Qt.red)
        format.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)

        for word_object in re.finditer(self.WORDS, text):
            if not self.dict.check(word_object.group()):
                self.setFormat(word_object.start(),
                               word_object.end() - word_object.start(), format)