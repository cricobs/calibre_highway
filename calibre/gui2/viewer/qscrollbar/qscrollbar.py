from PyQt5.QtWidgets import QScrollBar

from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class Qscrollbar(QScrollBar, Qwidget):
    def __init__(self, *args, **kwargs):
        super(Qscrollbar, self).__init__(*args, **kwargs)