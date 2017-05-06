import json
import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget

from calibre.gui2.viewer.library.filepath import filepath_relative
from calibre.gui2.viewer.qabstractlistmodel.qabstractlistmodelShortcut import \
    QabstractlistmodelShortcut
from calibre.gui2.viewer.qapplication.qapplication import Qapplication
from calibre.gui2.viewer.qwidget.qwidgetSearchReplace import QwidgetSearchReplace

I = I

with open(filepath_relative(sys.modules[__name__], "json")) as iput:
    SHORTCUTS = {
        name: (shortcuts, _(tooltip))
        for name, (shortcuts, tooltip) in json.load(iput)["shortcuts"].items()
        }


class QapplicationViewer(Qapplication):
    search = pyqtSignal(QWidget, str, bool)
    replace = pyqtSignal(QWidget, str, str, bool)
    appendMarkdown = pyqtSignal(str, dict)
    copyMarkdown = pyqtSignal(str, dict)
    selectionChanged = pyqtSignal()
    copyChanged = pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super(QapplicationViewer, self).__init__(*args, **kwargs)

        self.qabstractlistmodelShortcut = QabstractlistmodelShortcut(SHORTCUTS, 'shortcuts/viewer')
        self.qwidgetSearchReplace = QwidgetSearchReplace()

        self.setWindowIcon(QIcon(I('viewer.png')))

    def on_qwidget_selectionChanged(self):
        self.copyChanged.emit(bool(self.selected_text()))

    def append_markdown(self, options):
        text = self.selected_text()
        if text:
            self.appendMarkdown.emit(text, options)

    def copy_markdown(self, options):
        text = self.selected_text()
        if text:
            self.copyMarkdown.emit(text, options)

    def copy(self):
        self.focusWidget().copy()
