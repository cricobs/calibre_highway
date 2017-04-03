from PyQt5.QtCore import QTimer


class Qtimer(QTimer):
    def __init__(self, *args, **kwargs):
        super(Qtimer, self).__init__(*args, **kwargs)

    def restart(self):
        self.stop()
        self.start(self.interval())
