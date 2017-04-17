from PyQt5.QtCore import QSettings


class Qsettings(QSettings):
    def __init__(self, *args, **kwargs):
        super(Qsettings, self).__init__(*args, **kwargs)

        p = self.parent()
        if p:
            self.beginGroup(p.__class__.__name__)
