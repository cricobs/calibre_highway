from calibre.gui2.viewer.qsyntaxhighlighter.qsyntaxhighlighterSpellcheck import \
    QsyntaxhighlighterSpellcheck
from calibre.gui2.viewer.qsyntaxhighlighter.qsyntaxhighlighterMarkdown import \
    QsyntaxhighlighterMarkdown


class QsyntaxhighlighterSynopsis(QsyntaxhighlighterMarkdown, QsyntaxhighlighterSpellcheck):
    def __init__(self, parent=None, checker=None):
        super(QsyntaxhighlighterSynopsis, self).__init__(parent, checker=checker)

    def highlightBlock(self, text):
        QsyntaxhighlighterMarkdown.highlightBlock(self, text)
        QsyntaxhighlighterSpellcheck.highlightBlock(self, text)

