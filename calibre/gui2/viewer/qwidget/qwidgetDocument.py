from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class QwidgetDocument(Qwidget):
    def __init__(self, *args, **kwargs):
        super(QwidgetDocument, self).__init__(*args, **kwargs)

        self.parent().setCentralWidget(self)