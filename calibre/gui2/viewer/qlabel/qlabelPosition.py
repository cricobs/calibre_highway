from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QScrollBar

from calibre.gui2.viewer.qlabel.qlabel import Qlabel


class QlabelPosition(Qlabel):
    def __init__(self, *args, **kwargs):
        super(QlabelPosition, self).__init__(*args, **kwargs)

        self.style = '''
            QLabel {
                text-align: center;
                background-color: %s;
                color: %s;
                font-family: monospace;
                padding: 5px;
        }'''

    def set_style_options(self, background_color, color):
        self.setStyleSheet(self.style % (background_color, color))

    def update_position(self, scrollbar=True):
        if not self.isVisible():
            return

        height = self.parent().height() - self.height()
        width = self.parent().width() - self.width()
        if scrollbar:
            qscrollbars = self.parent().findChildren(QScrollBar)
            for q in qscrollbars:
                if q.orientation() == Qt.Vertical:
                    width -= q.width()
                    break

        self.move(width - 6, height - 6)

    def update_value(self, *args):
        if not self.isVisible():
            return

        try:
            value, maximum = args
        except ValueError:
            value, maximum = self.sender().value(), self.sender().maximum()

        self.setText(str(value))
        self.resize(self.sizeHint())
        self.update_position()
