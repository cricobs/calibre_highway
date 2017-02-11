from PyQt5.uic import loadUi

from PyQt5.QtCore import QObject

from calibre.library.filepath import filepath_relative


class Qobject(QObject):
    def __init__(self, *args, **kwargs):
        super(Qobject, self).__init__(*args, **kwargs)

        ui_path = filepath_relative(self, "ui")

        try:
            loadUi(ui_path, self)
        except IOError:
            pass