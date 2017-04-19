from PyQt5.QtGui import QSyntaxHighlighter

from calibre.gui2.viewer.qobject.qobject import Qobject


class Qsyntaxhighlighter(QSyntaxHighlighter, Qobject):
    def __init__(self, *args, **kwargs):
        super(Qsyntaxhighlighter, self).__init__(*args)
