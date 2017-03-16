from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QToolButton

from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class QwidgetSearch(Qwidget):
    def __init__(self, *args, **kwargs):
        super(QwidgetSearch, self).__init__(*args, **kwargs)

        self.search.initialize('viewer_search_history', help_text=_('Search Ebook'))
        self.hide()

    def keyPressEvent(self, qkeyevent):
        if qkeyevent == Qt.Key_Escape:
            self.hide()

        super(QwidgetSearch, self).keyPressEvent(qkeyevent)

    def addAction(self, action):
        super(QwidgetSearch, self).addAction(action)

        qtoolbutton = QToolButton(self)
        qtoolbutton.setText(action.text())
        qtoolbutton.setIcon(action.icon())
        qtoolbutton.setToolTip(action.toolTip())
        qtoolbutton.clicked.connect(action.trigger)

        self.horizontalLayoutToolButtons.addWidget(qtoolbutton)

