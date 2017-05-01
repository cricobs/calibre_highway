from PyQt5.QtCore import QEvent
from PyQt5.QtCore import pyqtSignal, QSize

from calibre.gui2.viewer.qwebpage.qwebpageFootnote import QwebpageFootnote
from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class QwidgetFootnote(Qwidget):
    follow_link = pyqtSignal()

    def __init__(self, parent=None):
        super(QwidgetFootnote, self).__init__(parent)

        self.view.installEventFilter(self)

        self.setToolTip("Double click on the footnote to scroll to it")

    def eventFilter(self, qobject, qevent):
        if qevent.type() == QEvent.MouseButtonDblClick:
            self.follow_link.emit()

        return super(QwidgetFootnote, self).eventFilter(qobject, qevent)

    def sizeHint(self):
        return QSize(400, 200)
