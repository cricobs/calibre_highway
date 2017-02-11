from PyQt5.QtWidgets import QWidget

from calibre.gui2.viewer.qobject.qobject import Qobject


class Qwidget(QWidget, Qobject):
    def __init__(self, *args, **kwargs):
        super(Qwidget, self).__init__(*args, **kwargs)
