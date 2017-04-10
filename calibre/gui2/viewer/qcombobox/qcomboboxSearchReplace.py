from PyQt5.QtCore import pyqtSignal

from calibre.gui2.viewer.qcombobox.qcombobox import Qcombobox
from calibre.gui2.viewer.qlineedit.qlineeditSearchReplace import QlineeditSearchReplace


class QcomboboxSearchReplace(Qcombobox):
    returnPressed = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(QcomboboxSearchReplace, self).__init__(*args, **kwargs)

        c = self.completer()
        c.setCompletionMode(c.PopupCompletion)

        self.qlineedit = QlineeditSearchReplace()
        self.qlineedit.returnPressed.connect(self.on_qlineedit_returnPressed)

        self.setLineEdit(self.qlineedit)

        self.insertItem(0, "zero")
        self.insertItem(1, "one")
        self.insertItem(2, "two")
        self.insertItem(3, "three")

        self.setEditText("")

    def on_qlineedit_returnPressed(self):
        text = self.sender().text()
        if text:
            self.returnPressed.emit(text)
