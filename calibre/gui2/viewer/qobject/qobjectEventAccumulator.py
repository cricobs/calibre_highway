import os

from PyQt5.QtCore import QObject, pyqtSignal


class QobjectEventAccumulator(QObject):
    got_file = pyqtSignal(object)

    def __init__(self):
        QObject.__init__(self)
        self.events = []

    def __call__(self, paths):
        for path in paths:
            if os.path.exists(path):
                self.events.append(path)
                self.got_file.emit(path)

    def flush(self):
        if self.events:
            self.got_file.emit(self.events[-1])
            self.events = []