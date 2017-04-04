from PyQt5.QtWidgets import QLineEdit

from calibre.gui2.viewer.qcombobox.qcombobox import Qcombobox


class QcomboboxQlineedit(Qcombobox):
    def __init__(self, *args, **kwargs):
        super(QcomboboxQlineedit, self).__init__(*args, **kwargs)

        self.setLineEdit(QLineEdit())
