from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QStyle

from calibre.gui2.viewer.qdockwidget.qdockwidget import Qdockwidget


class QdockwidgetFootnote(Qdockwidget):
    def __init__(self, *args, **kwargs):
        super(QdockwidgetFootnote, self).__init__(*args, **kwargs)

        self.qwidgetFootnote.close_view.connect(self.on_qwidgetFootnote_close_view)

        size = self.style().pixelMetric(QStyle.PM_ToolBarIconSize)
        style = """
            QToolButton {{
                border: none;
                width: {size}px;
                height: {size}px;
            }}
        """.format(**{"size": size})

        self.goto_button.setIcon(self.style().standardIcon(QStyle.SP_FileDialogContentsView))
        self.goto_button.setToolTip(_('Go to this footnote in the main view'))
        # self.goto_button.setStyleSheet(style)
        self.goto_button.setMaximumWidth(size)
        self.goto_button.setMaximumHeight(size)

        self.close_button.setIcon(self.style().standardIcon(QStyle.SP_DialogCloseButton))
        self.close_button.setToolTip(_('Close the footnotes window'))
        # self.close_button.setStyleSheet(style)
        self.close_button.setMaximumWidth(size)
        self.close_button.setMaximumHeight(size)

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
