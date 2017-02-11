from PyQt5.QtWidgets import QLineEdit

from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class Qlineedit(QLineEdit, Qwidget):
    def __init__(self, *args, **kwargs):
        super(Qlineedit, self).__init__(*args, **kwargs)
