from PyQt5.QtWidgets import QListWidget

from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class Qlistwidget(QListWidget, Qwidget):
    def __init__(self, *args, **kwargs):
        super(Qlistwidget, self).__init__(*args, **kwargs)