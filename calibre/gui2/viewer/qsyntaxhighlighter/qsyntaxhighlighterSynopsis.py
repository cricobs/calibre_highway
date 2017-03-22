from calibre.gui2.viewer.qsyntaxhighlighter.qsyntaxhighlighterSpellcheck import \
    QsyntaxhighlighterSpellcheck
from calibre.gui2.viewer.qsyntaxhighlighter.qsyntaxhighlighterMarkdown import \
    QsyntaxhighlighterMarkdown


class QsyntaxhighlighterSynopsis(QsyntaxhighlighterMarkdown, QsyntaxhighlighterSpellcheck):
    def __init__(self, *args, **kwargs):
        super(QsyntaxhighlighterSynopsis, self).__init__(*args, **kwargs)
