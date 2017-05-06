from PyQt5.QtCore import QRect
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QConicalGradient
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QWidget

from calibre.gui2.viewer.qwidget.qwidget import Qwidget


def draw_snake_spinner(painter, rect, angle, light, dark):
    painter.setRenderHint(QPainter.Antialiasing)

    if rect.width() > rect.height():
        delta = (rect.width() - rect.height()) // 2
        rect = rect.adjusted(delta, 0, -delta, 0)
    elif rect.height() > rect.width():
        delta = (rect.height() - rect.width()) // 2
        rect = rect.adjusted(0, delta, 0, -delta)
    disc_width = max(3, min(rect.width() // 10, 8))

    drawing_rect = QRect(rect.x() + disc_width, rect.y() + disc_width,
                         rect.width() - 2 * disc_width, rect.height() - 2 * disc_width)

    gap = 60  # degrees
    gradient = QConicalGradient(drawing_rect.center(), angle - gap // 2)
    gradient.setColorAt((360 - gap // 2) / 360.0, light)
    gradient.setColorAt(0, dark)

    pen = QPen(QBrush(gradient), disc_width)
    pen.setCapStyle(Qt.RoundCap)
    painter.setPen(pen)
    painter.drawArc(drawing_rect, angle * 16, (360 - gap) * 16)


class QwidgetProgressSpinner(QWidget):
    def __init__(self, parent=None, size=64, interval=10):
        QWidget.__init__(self, parent)
        self.setSizePolicy(QSizePolicy(
            QSizePolicy.GrowFlag | QSizePolicy.ShrinkFlag,
            QSizePolicy.GrowFlag | QSizePolicy.ShrinkFlag))
        self._size_hint = QSize(size, size)
        self.timer = t = QTimer(self)
        t.setInterval(interval)
        self.timer.timeout.connect(self.tick)
        self.loading_angle = 0
        pal = self.palette()
        self.dark = pal.color(pal.Text)
        self.light = pal.color(pal.Window)
        self.errored_out = False

    @property
    def animation_interval(self):
        return self.timer.interval()

    @animation_interval.setter
    def animation_interval(self, val):
        self.timer.setInterval(val)

    def heightForWidth(self, w):
        return w

    def set_colors(self, dark, light):
        self.dark, self.light = dark, light
        self.update()

    def start(self):
        self.loading_angle = 0
        self.timer.start()
        self.update()

    startAnimation = start

    def stop(self):
        self.timer.stop()
        self.loading_angle = 0
        self.update()

    stopAnimation = stop

    @property
    def is_animated(self):
        return self.timer.isActive()

    @is_animated.setter
    def is_animated(self, val):
        (self.start if val else self.stop)()

    def isAnimated(self):
        return self.is_animated

    def sizeHint(self):
        return self._size_hint

    def setSizeHint(self, val):
        if isinstance(val, int):
            val = QSize(val, val)
        self._size_hint = val
        self.update()

    setDisplaySize = setSizeHint

    def tick(self):
        self.loading_angle -= 2
        self.loading_angle %= 360
        self.update()

    def paintEvent(self, ev):
        if not self.errored_out:
            try:
                draw_snake_spinner(QPainter(self), self.rect(), self.loading_angle, self.light,
                                   self.dark)
            except Exception:
                import traceback
                traceback.print_exc()
                self.errored_out = True


class QwidgetProgress(Qwidget):
    def __init__(self, *args):
        super(QwidgetProgress, self).__init__(*args)

        self.setGeometry(0, 0, 300, 350)
        self.pi = QwidgetProgressSpinner(self)
        self.status = QLabel(self)
        self.status.setWordWrap(True)
        self.status.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.setVisible(False)
        self.pos = None

        self.parent().installEventFilter(self)

    def eventFilter(self, qobject, qevent):
        if qevent.type() == qevent.EnabledChange:
            if qobject.isEnabled():
                self.stop()
                qobject.unsetCursor()
                qobject.setFocus(Qt.PopupFocusReason)
            else:
                self.start()
                qobject.setCursor(Qt.BusyCursor)

        return super(QwidgetProgress, self).eventFilter(qobject, qevent)

    def start(self, msg=''):
        view = self.parent()
        pwidth, pheight = view.size().width(), view.size().height()
        self.resize(pwidth, min(pheight, 250))
        if self.pos is None:
            self.move(0, (pheight - self.size().height()) / 2.)
        else:
            self.move(self.pos[0], self.pos[1])
        self.pi.resize(self.pi.sizeHint())
        self.pi.move(int((self.size().width() - self.pi.size().width()) / 2.), 0)
        self.status.resize(self.size().width(),
                           self.size().height() - self.pi.size().height() - 10)
        self.status.move(0, self.pi.size().height() + 10)
        self.status.setText('<h1>' + msg + '</h1>')
        self.setVisible(True)
        self.pi.startAnimation()

    def stop(self):
        self.pi.stopAnimation()
        self.setVisible(False)
