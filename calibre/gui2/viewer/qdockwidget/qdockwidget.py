from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtWidgets import QWidget

from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class Qdockwidget(QDockWidget, Qwidget):
    def __init__(self, *args, **kwargs):
        super(Qdockwidget, self).__init__(*args, **kwargs)

        self.interval_hide = 6666

        self.setTitleBarWidget(self.qwidgettitlebar)
        self.setVisible(self.start_visible)

    @property
    def mode_activity(self):
        return True

    @property
    def mode_toggle(self):
        return True

    def qapplication_inactivityTimeout(self, interval):
        if self.mode_hide and interval == self.interval_hide:
            self.close()

    def showEvent(self, qshowevent):
        super(Qdockwidget, self).showEvent(qshowevent)

        self.auto_hide()
        self.raise_()

    @property
    def mode_hide(self):
        """
        close on_qapplication_inactivityTimeout
        :return:
        """
        return False

    def auto_hide(self):
        if self.mode_hide:
            self.qapplication.time_inactivity(self, False, True, self.interval_hide)

    @property
    def start_visible(self):
        return False

    @property
    def qwidgettitlebar(self):
        return QWidget()
