from PyQt5.QtCore import pyqtSignal

from calibre.gui2 import Application
from calibre.gui2.viewer.qtimer.qtimer import Qtimer


class Qapplication(Application):
    inactivityTimeout = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(Qapplication, self).__init__(*args, **kwargs)
        self.qtimerActivity = Qtimer(self)
        self.qtimerActivity.setSingleShot(True)
        self.qtimerActivity.timeout.connect(self.on_qtimerActivity_timeout)

        self.installEventFilter(self)

    def on_qtimerActivity_timeout(self):
        self.inactivityTimeout.emit()

    def eventFilter(self, qobject, qevent):
        if self.qtimerActivity.isActive():
            if qevent.type() == qevent.KeyPress or qevent.type() == qevent.MouseMove:
                self.activity_detected()

        return super(Qapplication, self).eventFilter(qobject, qevent)

    def activity_detected(self):
        self.qtimerActivity.restart()

    def inactivity_wait(self, timeout=6666):
        self.qtimerActivity.start(timeout)
