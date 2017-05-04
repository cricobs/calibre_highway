from PyQt5.QtWidgets import QPlainTextEdit

from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class Qplaintextedit(QPlainTextEdit, Qwidget):
    def __init__(self, *args, **kwargs):
        super(Qplaintextedit, self).__init__(*args, **kwargs)

    @property
    def mode_selection(self):
        return True
