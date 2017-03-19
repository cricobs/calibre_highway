from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon

from calibre.gui2.viewer.qdockwidget.qdockwidget import Qdockwidget


class QdockwidgetFootnote(Qdockwidget):
    def __init__(self, *args, **kwargs):
        super(QdockwidgetFootnote, self).__init__(*args, **kwargs)

        self.qwidgetFootnote.close_view.connect(self.on_qwidgetFootnote_close_view)

        self.goto_button.setIcon(QIcon(I('forward.png')))
        self.goto_button.setToolTip(_('Go to this footnote in the main view'))

        self.close_button.setIcon(QIcon(I('window-close.png')))
        self.close_button.setToolTip(_('Close the footnotes window'))

    @property
    def qwidgettitlebar(self):
        return self.qwidgetTitlebar

    @pyqtSlot()
    def on_goto_button_clicked(self):
        self.qwidgetFootnote.follow_link.emit()

    @pyqtSlot()
    def on_close_button_clicked(self):
        self.qwidgetFootnote.close_view.emit()

    @pyqtSlot()
    def on_qwidgetFootnote_close_view(self):
        self.close()
