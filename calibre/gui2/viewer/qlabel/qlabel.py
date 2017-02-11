from PyQt5.QtWidgets import QLabel

from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class Qlabel(QLabel, Qwidget):
    def __init__(self, *args, **kwargs):
        super(Qlabel, self).__init__(*args, **kwargs)
