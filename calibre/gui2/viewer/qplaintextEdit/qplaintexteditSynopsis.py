from PyQt5.QtCore import pyqtSignal

from calibre.gui2.viewer.qplaintextEdit.qplaintextedit import Qplaintextedit


class QplaintexteditSynopsis(Qplaintextedit):
    contentChanged = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(QplaintexteditSynopsis, self).__init__(*args, **kwargs)

    def setPlainText(self, p_str):
        super(QplaintexteditSynopsis, self).setPlainText(p_str)

        self.contentChanged.emit()