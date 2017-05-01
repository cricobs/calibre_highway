from PyQt5.QtCore import QEvent
from PyQt5.QtCore import pyqtSignal

from calibre.gui2.viewer.qwebpage.qwebpageFootnote import QwebpageFootnote
from calibre.gui2.viewer.qwebview.qwebview import Qwebview


class QwebviewFootnote(Qwebview):
    follow_link = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(QwebviewFootnote, self).__init__(*args, **kwargs)

        self.installEventFilter(self)

    def eventFilter(self, qobject, qevent):
        if qevent.type() == QEvent.MouseButtonDblClick:
            self.follow_link.emit()

        return super(QwebviewFootnote, self).eventFilter(qobject, qevent)

    def create_page(self):
        return QwebpageFootnote(self)
