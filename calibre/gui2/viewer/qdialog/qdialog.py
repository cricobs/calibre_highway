from PyQt5.QtWidgets import QDialog

from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class Qdialog(QDialog, Qwidget):
    def __init__(self, *args, **kwargs):
        super(Qdialog, self).__init__(*args, **kwargs)
