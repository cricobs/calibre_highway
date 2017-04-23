import json
import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

from calibre.gui2.viewer.library.filepath import filepath_relative
from calibre.gui2.viewer.qabstractlistmodel.qabstractlistmodelShortcut import \
    QabstractlistmodelShortcut
from calibre.gui2.viewer.qapplication.qapplication import Qapplication
from calibre.gui2.viewer.qwidget.qwidgetSearchReplace import QwidgetSearchReplace

with open(filepath_relative(sys.modules[__name__], "json")) as iput:
    SHORTCUTS = {
        name: (shortcuts, _(tooltip))
        for name, (shortcuts, tooltip) in json.load(iput)["shortcuts"].items()
        }


class QapplicationViewer(Qapplication):
    search = pyqtSignal(QWidget, str, bool)
    replace = pyqtSignal(QWidget, str, str, bool)

    def __init__(self, *args, **kwargs):
        super(QapplicationViewer, self).__init__(*args, **kwargs)

        self.qabstractlistmodelShortcut = QabstractlistmodelShortcut(SHORTCUTS, 'shortcuts/viewer')
        self.qwidgetSearchReplace = QwidgetSearchReplace()
