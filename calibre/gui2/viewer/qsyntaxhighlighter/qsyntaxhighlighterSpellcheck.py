import re

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCharFormat

from calibre.gui2.viewer.qsyntaxhighlighter.qsyntaxhighlighter import Qsyntaxhighlighter


class Checker(object):
    def __init__(self):
        super(Checker, self).__init__()

    def check(self, text):
        return False


class QsyntaxhighlighterSpellcheck(Qsyntaxhighlighter):
    WORDS = u'(?iu)[\w\']+'

    def __init__(self, parent=None, checker=None, *args, **kwargs):
        super(QsyntaxhighlighterSpellcheck, self).__init__(parent, *args, **kwargs)
        self.checker = checker or Checker()

    def set_checker(self, checker):
        self.checker = checker

    def highlightBlock(self, text):
        pass
    #     text = unicode(text)
    #
    #     format = QTextCharFormat()
    #     format.setUnderlineColor(Qt.red)
    #     format.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)
    #
    #     for w in re.finditer(self.WORDS, text):
    #         if not self.checker.check(w.group()):
    #             self.setFormat(w.start(), w.end() - w.start(), format)
