from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWebKitWidgets import QWebView, QWebPage

from calibre.gui2.viewer.qwebpage.qwebpagePreview import QwebpagePreview
from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class Qwebview(QWebView, Qwidget):
    pageChange = pyqtSignal(QWebPage)

    def __init__(self, *args, **kwargs):
        super(Qwebview, self).__init__(*args, **kwargs)

        self.setPage(self.create_page())

    def create_page(self):
        return QwebpagePreview(self)

    def search(self, search, backwards=False):
        self.findText(search)

    def setPage(self, qwebpage):
        super(Qwebview, self).setPage(qwebpage)
        self.pageChange.emit(qwebpage)

    def contextMenuEvent(self, qevent):
        menu = self.page().createStandardContextMenu()
        if not menu.exec_(qevent.globalPos()):
            super(Qwebview, self).contextMenuEvent(qevent)

    @property
    def mode_search(self):
        return self.SEARCH

    @property
    def selected_text(self):
        return self.page().selectedText().replace(u'\u00ad', u'').strip()

    @property
    def mode_selection(self):
        return True
