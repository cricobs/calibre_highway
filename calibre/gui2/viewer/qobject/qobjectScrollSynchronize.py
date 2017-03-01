from PyQt5.QtCore import QPoint
from PyQt5.QtCore import Qt
from PyQt5.QtWebKitWidgets import QWebView, QWebPage
from PyQt5.QtWidgets import QAbstractSlider
from PyQt5.QtWidgets import QPlainTextEdit

from calibre.gui2.viewer.qobject.qobject import Qobject


class QobjectScrollSynchronize(Qobject):
    def __init__(self, *qwidgets, **kwargs):
        super(QobjectScrollSynchronize, self).__init__(**kwargs)

        self.qwidgets = qwidgets

        for q in qwidgets:
            if isinstance(q, QPlainTextEdit):
                signal = q.verticalScrollBar().sliderMoved
            elif isinstance(q, QWebView):
                signal = q.page().scrollRequested
            else:
                raise NotImplementedError

            signal.connect(self.on_qwidget_signal)

    def on_qwidget_signal(self):
        for q in self.qwidgets:
            if isinstance(q, QPlainTextEdit)and q.verticalScrollBar() is self.sender():
                continue
            elif isinstance(q, QWebView) and q.page() is self.sender():
                continue

            self.update_qwidget(self.sender(), q)

    def get_height(self, q):
        if isinstance(q, QAbstractSlider):
            return q.maximum()
        elif isinstance(q, QWebPage):
            return q.mainFrame().scrollBarMaximum(Qt.Vertical)
        elif isinstance(q, QWebView):
            return self.get_height(q.page())
        elif isinstance(q, QPlainTextEdit):
            return self.get_height(q.verticalScrollBar())

        raise NotImplementedError

    def get_position(self, q):
        if isinstance(q, QAbstractSlider):
            return q.sliderPosition()
        elif isinstance(q, QWebPage):
            return q.mainFrame().scrollPosition().y()
        elif isinstance(q, QWebView):
            return self.get_position(q.page())
        elif isinstance(q, QPlainTextEdit):
            return self.get_position(q.verticalScrollBar())

        raise NotImplementedError

    def set_position(self, q, position):
        if isinstance(q, QWebView):
            q.page().blockSignals(True)
            q.page().mainFrame().setScrollPosition(QPoint(0, position))
            q.page().blockSignals(False)
        elif isinstance(q, QPlainTextEdit):
            q.verticalScrollBar().blockSignals(True)
            q.verticalScrollBar().setValue(position)
            q.verticalScrollBar().blockSignals(False)
        else:
            raise NotImplementedError

    def update_qwidget(self, source, target):
        s_height = self.get_height(source)
        s_position = self.get_position(source)

        t_height = self.get_height(target)
        t_position = int(s_position * float(t_height) / s_height)

        self.set_position(target, t_position)
