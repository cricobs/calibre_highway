from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon

from calibre.gui2 import error_dialog
from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class QwidgetContentSearch(Qwidget):
    def __init__(self, *args, **kwargs):
        super(QwidgetContentSearch, self).__init__(*args, **kwargs)

        self.search.initialize('viewer_toc_search_history', help_text=_('Search Content'))
        self.toolButton.setIcon(QIcon(I('search.png')))

    @pyqtSlot(bool)
    def on_toolButton_clicked(self, checked):
        self.search.do_search()

    @pyqtSlot(object)
    def on_search_search(self, text):
        if not text or not text.strip():
            return
        index = self.toc_view.model().search(text)
        if index.isValid():
            self.toc_view.searched.emit(index)
        else:
            error_dialog(self.toc_view, _('No matches found'), _(
                'There are no Table of Contents entries matching: %s') % text, show=True)
        self.search.search_done(True)
