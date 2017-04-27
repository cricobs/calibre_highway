from PyQt5.QtWebKitWidgets import QWebPage

from calibre.gui2.viewer.qdockwidget.qdockwidget import Qdockwidget
from calibre.gui2.viewer.qwidget.qwidgetQwebinspector import QwidgetQwebinspector


class QdockwidgetQwebinspector(Qdockwidget):
    def __init__(self, *args, **kwargs):
        super(QdockwidgetQwebinspector, self).__init__(*args, **kwargs)

        self._windowTitle = None
        self.actions = {}

        for qwebpage in self.parent().findChildren(QWebPage):
            self.add_qwebpage(qwebpage)

    def setWindowTitle(self, p_str):
        super(QdockwidgetQwebinspector, self).setWindowTitle(p_str)
        try:
            if self._windowTitle is None:
                self._windowTitle = p_str
        except AttributeError:
            pass

    def add_qwebpage(self, qwebpage):
        qwebpage.view().pageChange.connect(self.on_view_pageChange)
        qwebpage.settings().setAttribute(qwebpage.settings().DeveloperExtrasEnabled, True)

        action = qwebpage.action(qwebpage.InspectElement)
        action.triggered.connect(self.on_InspectElement_triggered)

        qwidgetQwebinspector = QwidgetQwebinspector(self)
        qwidgetQwebinspector.qwebinspector.setPage(qwebpage)

        self.actions[action] = qwidgetQwebinspector

        self.qstackedwidget.addWidget(qwidgetQwebinspector)

    def on_view_pageChange(self, qwebpage):
        self.add_qwebpage(qwebpage)

    def on_InspectElement_triggered(self):
        qwidgetQwebinspector = self.actions[self.sender()]

        self.setWindowTitle("{0}: {1}".format(
            self._windowTitle, qwidgetQwebinspector.qwebinspector.page().view().__class__.__name__))
        self.qstackedwidget.setCurrentWidget(qwidgetQwebinspector)
        self.show()
        self.setMinimumHeight(0)  # agtft not starting with correct size)

    @property
    def qwidgettitlebar(self):
        return None
