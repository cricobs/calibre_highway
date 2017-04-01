from PyQt5.QtCore import QEvent
from PyQt5.QtCore import pyqtSignal, QSize

from calibre.gui2.viewer.qwebpage.qwebpageFootnote import QwebpageFootnote
from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class QwidgetFootnote(Qwidget):
    follow_link = pyqtSignal()

    def __init__(self, parent=None):
        super(QwidgetFootnote, self).__init__(parent)

        self.qwebpagefootnote = QwebpageFootnote(self.view)

        self.view.setPage(self.qwebpagefootnote)
        self.view.installEventFilter(self)

        self.setToolTip("Double click on the footnote to it on the main view")

    def eventFilter(self, qobject, qevent):
        if qevent.type() == QEvent.MouseButtonDblClick:
            self.follow_link.emit()

        return super(QwidgetFootnote, self).eventFilter(qobject, qevent)

    def on_qwebpagefootnote_doubleClick(self):
        print ("mama")

    def page(self):
        return self.qwebpagefootnote

    def mouseDoubleClickEvent(self, qmouseevent):
        super(QwidgetFootnote, self).mouseDoubleClickEvent(qmouseevent)

        print ("mama")

    def sizeHint(self):
        return QSize(400, 200)
