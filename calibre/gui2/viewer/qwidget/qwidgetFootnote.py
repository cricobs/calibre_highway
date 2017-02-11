from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QToolButton

from calibre.gui2.viewer.qwebpage.qwebpageFootnote import QwebpageFootnote


class QwidgetFootnote(QWidget):
    follow_link = pyqtSignal()
    close_view = pyqtSignal()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.l = l = QHBoxLayout(self)
        self.vl = vl = QVBoxLayout()
        self.view = v = QWebView(self)
        self._page = QwebpageFootnote(v)
        v.setPage(self._page)
        l.addWidget(v), l.addLayout(vl)
        self.goto_button = b = QToolButton(self)
        b.setIcon(QIcon(I('forward.png'))), b.setToolTip(_('Go to this footnote in the main view'))
        b.clicked.connect(self.follow_link)
        vl.addWidget(b)
        self.close_button = b = QToolButton(self)
        b.setIcon(QIcon(I('window-close.png'))), b.setToolTip(_('Close the footnotes window'))
        b.clicked.connect(self.close_view)
        vl.addWidget(b)

    def page(self):
        return self._page

    def sizeHint(self):
        return QSize(400, 200)