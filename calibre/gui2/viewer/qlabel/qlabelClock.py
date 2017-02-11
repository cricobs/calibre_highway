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

        self.setText('99:99')
        self.setVisible(False)

    def set_style_options(self, background_color, color):
        self.setStyleSheet(self.style % (background_color, color))
