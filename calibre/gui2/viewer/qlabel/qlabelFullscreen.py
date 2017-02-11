from calibre.gui2.viewer.qlabel.qlabel import Qlabel


class QlabelFullscreen(Qlabel):
    def __init__(self, *args, **kwargs):
        super(QlabelFullscreen, self).__init__(*args, **kwargs)

        self.setText('''
                <center>
                <h1>%s</h1>
                <h3>%s</h3>
                <h3>%s</h3>
                <h3>%s</h3>
                </center>
                ''' % (_('Full screen mode'),
                       _('Right click to show controls'),
                       _('Tap in the left or right page margin to turn pages'),
                       _('Press Esc to quit'))
                     )
        self.setVisible(False)
        self.final_height = 200
