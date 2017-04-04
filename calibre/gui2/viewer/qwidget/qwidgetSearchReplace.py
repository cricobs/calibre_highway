from PyQt5.QtWidgets import QScrollBar

from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class QwidgetSearchReplace(Qwidget):
    TOP_RIGHT = 0

    def __init__(self, parent=None, relative=None, position=TOP_RIGHT, *args, **kwargs):
        super(QwidgetSearchReplace, self).__init__(parent, *args, **kwargs)

        self._relative = None
        self._position = position
        self._position_width = None

        self.relative = relative
    
        self.hide()

    @property
    def relative(self):
        return self._relative

    @relative.setter
    def relative(self, relative):
        if self._relative:
            self._relative.removeEventFilter(self)

        self._relative = relative or self.parent()
        self._relative.installEventFilter(self)

    @property
    def position_width(self):
        if self._position_width is None:
            self._position_width = QScrollBar().sizeHint().width()
            self._position_width += self.layout().contentsMargins().left()
            self._position_width += self.width()

        return self._position_width

    def position_top_right(self):
        width = self.relative.width() - self.position_width
        height = 0

        return width, height

    @property
    def position(self):
        if self._position == self.TOP_RIGHT:
            return self.position_top_right()

        raise NotImplementedError

    def update_position(self):
        self.move(*self.position)

    def eventFilter(self, qobject, qevent):
        if qevent.type() == qevent.Resize:
            self.update_position()

        return super(QwidgetSearchReplace, self).eventFilter(qobject, qevent)
