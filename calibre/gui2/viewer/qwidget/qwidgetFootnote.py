from PyQt5.QtCore import QSize

from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class QwidgetFootnote(Qwidget):
    def __init__(self, parent=None):
        super(QwidgetFootnote, self).__init__(parent)

        self.setToolTip("Double click on the footnote to scroll to it")

    def sizeHint(self):
        return QSize(400, 200)
