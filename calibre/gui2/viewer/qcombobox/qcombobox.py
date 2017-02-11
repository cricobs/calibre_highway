from PyQt5.QtWidgets import QComboBox

from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class Qcombobox(QComboBox, Qwidget):
    def __init__(self, *args, **kwargs):
        super(Qcombobox, self).__init__(*args, **kwargs)