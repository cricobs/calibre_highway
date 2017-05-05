from collections import defaultdict

from PyQt5.QtCore import QObject
from PyQt5.QtCore import QSignalMapper
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget

from calibre.gui2 import Application
from calibre.gui2.viewer.qtimer.qtimer import Qtimer


class Qapplication(Application):
    loadedUi = pyqtSignal(QObject)
    inactivityTimeout = pyqtSignal(QWidget, int)
    activity = pyqtSignal()
    qactionAdded = pyqtSignal(QObject, QAction)

    def __init__(self, *args, **kwargs):
        super(Qapplication, self).__init__(*args, **kwargs)

        self.qactions = defaultdict(list)
        self.targets = defaultdict(list)

        self.qsignalmapper = QSignalMapper(self)
        self.qsignalmapper.mapped[QWidget].connect(self.on_qsignalmapper_mapped)

        self.installEventFilter(self)

    def copy_text(self, text):
        self.clipboard().setText(text)

    def selected_text(self):
        try:
            return self.focusWidget().selected_text
        except AttributeError:
            pass

    def topLevelWidgets(self, type=None):
        topLevelWidgets = super(Qapplication, self).topLevelWidgets()
        if type:
            return list(filter(lambda t: isinstance(t, type), topLevelWidgets))
        return topLevelWidgets

    def topLevelWidget(self, type=None):
        type = QMainWindow if type is None else type
        topLevelWidgets = self.topLevelWidgets(type)

        try:
            return topLevelWidgets[0]
        except IndexError:
            return None

    def eventFilter(self, qobject, qevent):
        if qevent.type() == qevent.ActionAdded:
            qaction = qevent.action()
            if not qaction.isSeparator():
                parents = getattr(qaction, "parents", [])
                for parent in parents:
                    qs = self.qactions[parent]
                    if qaction not in qs:
                        qs.append(qaction)

                self.qactionAdded.emit(qaction.parent(), qaction)
        elif qevent.type() == qevent.MouseMove:
            self.activity_detected()

        return super(Qapplication, self).eventFilter(qobject, qevent)

    def activity_detected(self):
        for target, values in self.targets.items():
            for (qtimer, cycle, unique) in values:
                qtimer.restart()

        self.activity.emit()

    def on_qsignalmapper_mapped(self, target):
        qtimer = self.sender().sender()
        qtimers = []
        for (q, cycle, unique) in self.targets[target]:
            if (q != qtimer) or cycle:
                qtimers.append((q, cycle, unique))

        if qtimers:
            self.targets[target] = qtimers
        else:
            del self.targets[target]

        self.inactivityTimeout.emit(target, qtimer.interval())

    def time_inactivity(self, target, cycle=True, unique=True, interval=6666):
        """
        start a qtimer for inactivity
        :param target: the object that will be used to identify the inactivityTimeout signal with
        :param cycle: qtimer won't be removed on_qsignalmapper_mapped; on activity_detected it
        will be restarted.
        :param unique: a single qtimer with given interval for that target
        :param interval: interval for qtimer
        :return:
        """
        qtimer = Qtimer(self)
        qtimer.setSingleShot(True)
        qtimer.timeout.connect(self.qsignalmapper.map)

        self.qsignalmapper.setMapping(qtimer, target)

        if unique:
            qtimers = []
            for (q, cycle, unique) in self.targets[target]:
                if q.interval() != interval:
                    qtimers.append((q, cycle, unique))
                else:
                    q.stop()

            self.targets[target] = qtimers

        self.targets[target].append((qtimer, cycle, unique))

        qtimer.start(interval)
