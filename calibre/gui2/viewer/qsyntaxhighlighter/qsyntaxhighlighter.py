from PyQt5.QtGui import QSyntaxHighlighter


class Qsyntaxhighlighter(QSyntaxHighlighter):
    def __init__(self, *args, **kwargs):
        super(Qsyntaxhighlighter, self).__init__(*args)
