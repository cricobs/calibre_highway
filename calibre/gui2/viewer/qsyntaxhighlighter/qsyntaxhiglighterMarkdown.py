import json

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QTextCharFormat

from calibre.gui2.viewer.qsyntaxhighlighter.qsyntaxhighlighter import Qsyntaxhighlighter
from calibre.library.filepath import filepath_relative


class QsyntaxhighlighterMarkdown(Qsyntaxhighlighter):
    def __init__(self, parent=None):
        super(QsyntaxhighlighterMarkdown, self).__init__(parent)

        self.formats = []

        with open(filepath_relative(self, "json")) as iput:
            self.add_formats(json.load(iput))

    def add_formats(self, rules):
        for name, values in rules.items():
            self.add_format(**values)

    def add_format(self, expression, color=None, italic=None, size=None, weight=None):
        qtextcharformat = QTextCharFormat()
        if color:
            qtextcharformat.setForeground(QColor(color))
        if italic:
            qtextcharformat.setFontItalic(italic)
        if size:
            qtextcharformat.setFontPointSize(size)
        if weight:
            qtextcharformat.setFontWeight(weight)

        self.formats.append((QRegExp(expression), qtextcharformat))

    def highlightBlock(self, text):
        for pattern, format in self.formats:
            qregexp = QRegExp(pattern)
            index = qregexp.indexIn(text)
            while index >= 0:
                length = qregexp.matchedLength()
                self.setFormat(index, length, format)
                index = qregexp.indexIn(text, index + length)

        self.setCurrentBlockState(0)
