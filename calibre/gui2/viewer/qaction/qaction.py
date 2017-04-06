from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction


class Qaction(QAction):
    def __init__(self, *args, **kwargs):
        super(Qaction, self).__init__(*args, **kwargs)

        self.parents = []

    def setIcon(self, qicon):
        super(Qaction, self).setIcon(QIcon(I(qicon)))
