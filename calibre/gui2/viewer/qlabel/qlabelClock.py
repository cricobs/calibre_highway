from PyQt5.QtCore import QTime
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QScrollBar

from calibre.gui2.viewer.qlabel.qlabel import Qlabel


class QlabelClock(Qlabel):
    def __init__(self, *args, **kwargs):
        super(QlabelClock, self).__init__(*args, **kwargs)

        self.style = '''
            QLabel {
                text-align: center;
                border-width: 1px;
                border-style: solid;
                border-radius: 8px;
                background-color: %s;
                color: %s;
                font-family: monospace;
                font-size: larger;
                padding: 5px;
        }'''

        self.qtimerTime = QTimer(self)
        self.qtimerTime.timeout.connect(self.update_time)

        self.setText('99:99')
        self.setVisible(False)

        self.window().installEventFilter(self)
        self.parent().installEventFilter(self)

    def eventFilter(self, qobject, qevent):
        if qevent.type() == qevent.Resize:
            self.update_position()
        elif qevent.type() == qevent.WindowStateChange:
            self.setVisible(qobject.isFullScreen() and self.isEnabled())
            self.update_position()

        return super(QlabelClock, self).eventFilter(qobject, qevent)

    def update_position(self, scrollbar=True):
        if not self.isVisible():
            return

        width = self.parent().width() - self.width()
        if scrollbar:
            qscrollbars = self.parent().findChildren(QScrollBar)
            for q in qscrollbars:
                if q.orientation() == Qt.Vertical:
                    width -= q.width()
                    break

        self.move(width - 6, 6)

    def set_style_options(self, background_color, color):
        self.setStyleSheet(self.style % (background_color, color))

    def update_time(self):
        self.setText(QTime.currentTime().toString(Qt.SystemLocaleShortDate))

    def showEvent(self, qshowevent):
        super(QlabelClock, self).showEvent(qshowevent)

        self.update_time()
        self.resize(self.sizeHint())
        self.qtimerTime.start(1000)

    def hideEvent(self, qhideevent):
        super(QlabelClock, self).hideEvent(qhideevent)

        self.qtimerTime.stop()
