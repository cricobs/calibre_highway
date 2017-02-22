from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPlainTextEdit

from calibre.gui2.viewer.qobject.qobject import Qobject


class QobjectScrollPosition(Qobject):
    def __init__(self, parent, *args, **kwargs):
        super(QobjectScrollPosition, self).__init__(parent, *args, **kwargs)

        self.position = None

        self.parent().positionSave.connect(self.on_parent_positionSave)
        self.parent().positionLoad.connect(self.on_parent_positionLoad)

        QApplication.instance().aboutToQuit.connect(self.on_qapplication_aboutToQuit)

    def current_position(self):
        if isinstance(self.parent(), QPlainTextEdit):
            return self.parent().verticalScrollBar().value()
        elif isinstance(self.parent(), QWebView):
            return self.parent().page().mainFrame().scrollBarValue(Qt.Vertical)

    def on_qapplication_aboutToQuit(self):
        from calibre.gui2.viewer.qmainwindow.qmainwindowEbook import vprefs

        vprefs.set(self.parent().objectName() + "_position", self.current_position())

    def on_parent_positionSave(self):
        if self.position is None:
            from calibre.gui2.viewer.qmainwindow.qmainwindowEbook import vprefs

            self.position = vprefs.get(self.parent().objectName() + "_position")
        else:
            self.position = self.current_position()

    def on_parent_positionLoad(self):
        if isinstance(self.parent(), QPlainTextEdit):
            QTimer().singleShot(
                111, lambda: self.parent().verticalScrollBar().setValue(self.position))

        elif isinstance(self.parent(), QWebView):
            self.parent().page().mainFrame().setScrollBarValue(Qt.Vertical, self.position)
