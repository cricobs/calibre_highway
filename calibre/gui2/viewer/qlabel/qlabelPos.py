from calibre.gui2.viewer.qlabel.qlabel import Qlabel


class QlabelPos(Qlabel):
    def __init__(self, *args, **kwargs):
        super(QlabelPos, self).__init__(*args, **kwargs)

        self.style = '''
            QLabel {
                text-align: center;
                background-color: %s;
                color: %s;
                font-family: monospace;
                padding: 5px;
        }'''

        # self.setText('2000/4000')
        # self.setVisible(False)

    def set_style_options(self, background_color, color):
        self.setStyleSheet(self.style % (background_color, color))
