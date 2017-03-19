from PyQt5.QtCore import pyqtSignal, QSize, pyqtSlot
from PyQt5.QtGui import QIcon

from calibre.gui2.viewer.qwebpage.qwebpageFootnote import QwebpageFootnote
from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class QwidgetFootnote(Qwidget):
    follow_link = pyqtSignal()
    close_view = pyqtSignal()

    def __init__(self, parent=None):
        super(QwidgetFootnote, self).__init__(parent)

        self._page = QwebpageFootnote(self.view)
        self.view.setPage(self._page)

    def page(self):
        return self._page

    def sizeHint(self):
        return QSize(400, 200)
