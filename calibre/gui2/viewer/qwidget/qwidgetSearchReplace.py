from PyQt5.QtCore import QRect
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class QwidgetSearchReplace(Qwidget):
    TOP = 0

    def __init__(self, parent=None, relative=None, position=TOP, *args, **kwargs):
        super(QwidgetSearchReplace, self).__init__(parent, *args, **kwargs)

        self._relative = None
        self._position = position
        self._position_width = None

        self.relative = relative

        self.qapplication = QApplication.instance()
        self.qapplication.focusChanged.connect(self.on_qapplication_focusChanged)

    def on_qapplication_focusChanged(self, old, now):
        try:
            is_search_replace = now.is_search_replace
        except AttributeError:
            pass
        else:
            if is_search_replace:
                self.setParent(now)

    @property
    def is_visibility_tracked(self):
        return True

    def setParent(self, qwidget, qt_windowflags=Qt.Widget):
        if qwidget == self.parent():
            return

        super(QwidgetSearchReplace, self).setParent(qwidget, qt_windowflags)

        self.relative = qwidget

    @property
    def relative(self):
        return self._relative

    @relative.setter
    def relative(self, relative):
        if self._relative:
            self._relative.removeEventFilter(self)

        self._relative = relative or self.parent()

        if self._relative:
            self._relative.installEventFilter(self)

        self.update_position()

    def position_top(self):
        qrect = self.relative.rect()
        try:
            width = self.relative.page().mainFrame().contentsSize().width()
        except:
            pass
        else:
            if width < qrect.width():
                qrect.setWidth(width)
        try:
            qrect = self.relative.viewport().rect()
        except:
            pass

        qrect.setHeight(self.height())
        return qrect

    @property
    def position(self):
        if self._position == self.TOP:
            return self.position_top()

        raise NotImplementedError

    def update_position(self):
        if self.relative:
            self.setGeometry(self.position)

    def eventFilter(self, qobject, qevent):
        if qevent.type() == qevent.Resize:
            self.update_position()

        return super(QwidgetSearchReplace, self).eventFilter(qobject, qevent)
