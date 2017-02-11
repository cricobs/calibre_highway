import textwrap

from PyQt5.QtCore import QRegExp
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QRegExpValidator

from calibre.gui2.viewer.qlineedit.qlineedit import Qlineedit


class QLineeditReference(Qlineedit):
    goto = pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super(QLineeditReference, self).__init__(*args, **kwargs)

        self.setValidator(QRegExpValidator(QRegExp(r'\d+\.\d+'), self))
        self.setToolTip(textwrap.fill('<p>' + _(
            'Go to a reference. To get reference numbers, use the <i>reference '
            'mode</i>, by clicking the reference mode button in the toolbar.')))
        if hasattr(self, 'setPlaceholderText'):
            self.setPlaceholderText(_('Reference'))

        self.editingFinished.connect(self.editing_finished)

    def editing_finished(self):
        text = unicode(self.text())
        self.setText('')
        self.goto.emit(text)
