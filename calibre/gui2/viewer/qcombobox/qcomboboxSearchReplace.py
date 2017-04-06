from PyQt5.QtCore import pyqtSignal

from calibre.gui2.viewer.qcombobox.qcombobox import Qcombobox
from calibre.gui2.viewer.qlineedit.qlineeditSearchReplace import QlineeditSearchReplace


class QcomboboxSearchReplace(Qcombobox):
    returnPressed = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(QcomboboxSearchReplace, self).__init__(*args, **kwargs)

        self.qlineedit = QlineeditSearchReplace()
        self.qlineedit.returnPressed.connect(self.on_qlineEdit_returnPressed)

        self.setLineEdit(self.qlineedit)

    def on_qlineEdit_returnPressed(self):
        self.returnPressed.emit(self.sender().text())
