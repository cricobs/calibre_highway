from PyQt5.QtWidgets import QTreeView

from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class Qtreeview(QTreeView, Qwidget):
    def __init__(self, *args, **kwargs):
        super(Qtreeview, self).__init__(*args, **kwargs)