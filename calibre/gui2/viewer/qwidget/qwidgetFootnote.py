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

        self.goto_button.setIcon(QIcon(I('forward.png')))
        self.goto_button.setToolTip(_('Go to this footnote in the main view'))

        self.close_button.setIcon(QIcon(I('window-close.png')))
        self.close_button.setToolTip(_('Close the footnotes window'))

    @pyqtSlot()
    def on_goto_button_clicked(self):
        self.follow_link.emit()

    @pyqtSlot()
    def on_close_button_clicked(self):
        self.close_view.emit()

    def page(self):
        return self._page

    def sizeHint(self):
        return QSize(400, 200)
