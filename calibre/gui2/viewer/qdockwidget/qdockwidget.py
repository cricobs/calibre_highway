from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtWidgets import QWidget

from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class Qdockwidget(QDockWidget, Qwidget):
    def __init__(self, *args, **kwargs):
        super(Qdockwidget, self).__init__(*args, **kwargs)

        self.interval_hide = 6666

        self.setTitleBarWidget(self.qwidgettitlebar)
        self.setVisible(self.start_visible)

        self.qapplication = QApplication.instance()
        self.qapplication.inactivityTimeout.connect(self.on_qapplication_inactivityTimeout)

        self.toggleViewAction().triggered.connect(self.on_toggleViewAction_triggered)

    def on_qapplication_inactivityTimeout(self, target, interval):
        if target != self:
            return

        if self.is_auto_hide and interval == self.interval_hide:
            self.close()

    def on_toggleViewAction_triggered(self, checked):
        if checked:
            self.auto_hide()

    @property
    def is_auto_hide(self):
        return False

    def auto_hide(self):
        if self.is_auto_hide:
            self.qapplication.qtimer_inactivity(self, False, True, self.interval_hide)

    def show(self):
        super(Qdockwidget, self).show()
        self.auto_hide()

    def setVisible(self, bool):
        super(Qdockwidget, self).setVisible(bool)
        if bool:
            self.auto_hide()

    @property
    def start_visible(self):
        return False

    @property
    def qwidgettitlebar(self):
        return QWidget()

    def setVisible(self, visible):
        super(Qdockwidget, self).setVisible(visible)

        if visible:
            self.raise_()
