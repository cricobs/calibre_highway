from PyQt5.QtCore import QAbstractListModel

from calibre.gui2.viewer.qobject.qobject import Qobject
from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class Qabstractlistmodel(QAbstractListModel, Qobject):
    def __init__(self, *args, **kwargs):
        super(Qabstractlistmodel, self).__init__(*args, **kwargs)