from PyQt5.QtWebKitWidgets import QWebPage

from calibre.gui2.viewer.qdockwidget.qdockwidget import Qdockwidget
from calibre.gui2.viewer.qwidget.qwidgetQwebinspector import QwidgetQwebinspector


class QdockwidgetQwebinspector(Qdockwidget):
    def __init__(self, *args, **kwargs):
        super(QdockwidgetQwebinspector, self).__init__(*args, **kwargs)

        for qwebpage in self.parent().findChildren(QWebPage):
            self.add_qwebpage(qwebpage)

    def add_qwebpage(self, qwebpage):
        qwebpage.view().pageChange.connect(self.on_view_pageChange)
        qwebpage.settings().setAttribute(qwebpage.settings().DeveloperExtrasEnabled, True)

        qwidgetQwebinspector = QwidgetQwebinspector(self)

        qwebinspector = qwidgetQwebinspector.qwebinspector
        qwebinspector.setPage(qwebpage)

        action = qwebpage.action(qwebpage.InspectElement)
        action.triggered.connect(self.on_InspectElement_triggered)
        action.setData(qwidgetQwebinspector)

        self.qstackedwidget.addWidget(qwidgetQwebinspector)

    def on_view_pageChange(self, qwebpage):
        self.add_qwebpage(qwebpage)

    def on_InspectElement_triggered(self):
        self.show()
        self.setMinimumHeight(0)  # hack not starting with correct size
        self.qstackedwidget.setCurrentIndex(self.qstackedwidget.indexOf(self.sender().data()))

    @property
    def qwidgettitlebar(self):
        return None