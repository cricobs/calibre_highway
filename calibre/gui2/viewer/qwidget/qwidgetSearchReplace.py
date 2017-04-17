from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt, pyqtSlot

from calibre.gui2.viewer.qwidget.qwidget import Qwidget


# todo
#  - store relative search/replace history in qsettings

class QwidgetSearchReplace(Qwidget):
    TOP = 0

    def __init__(self, parent=None, relative=None, position=TOP, *args, **kwargs):
        super(QwidgetSearchReplace, self).__init__(parent, *args, **kwargs)

        self._relative = None
        self._position = position
        self._position_width = None

        self.relative = relative

        self.qapplication.focusChanged.connect(self.on_qapplication_focusChanged)

    def showEvent(self, qshowevent):
        super(QwidgetSearchReplace, self).showEvent(qshowevent)

        self.qcomboboxSearch.lineEdit().setFocus()

    @pyqtSlot(str)
    def on_qcomboboxSearch_returnPressed(self, text):
        self.qapplication.search.emit(self.relative, text)
        self.hide_and_show()

    def hide_and_show(self):  # agtft Qwebview not repainting correctly on scroll
        self.hide()
        QTimer.singleShot(0, self.show)

    @pyqtSlot(str)
    def on_qcomboboxReplace_returnPressed(self, text):
        self.qapplication.replace.emit(self.relative, self.qcomboboxSearch.lineEdit().text(), text)
        self.hide_and_show()

    def on_qapplication_focusChanged(self, old, now):
        try:
            mode_search = now.mode_search
        except AttributeError:
            pass
        else:
            if mode_search ^ self.NONE:
                self.setParent(now)

    @property
    def mode_visibility(self):
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
            self.qcomboboxSearch.setVisible(self._relative.mode_search & self.SEARCH)
            self.qcomboboxReplace.setVisible(self._relative.mode_search & self.REPLACE)

        self.update_position()

    def position_top(self):
        qrect = self.relative.rect()
        try:  # QWebView
            width = self.relative.page().mainFrame().contentsSize().width()
        except:
            pass
        else:
            if width < qrect.width():
                qrect.setWidth(width)
        try:  # QTextEdit
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
