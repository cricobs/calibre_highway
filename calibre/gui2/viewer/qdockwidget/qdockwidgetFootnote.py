from calibre.gui2.viewer.qdockwidget.qdockwidget import Qdockwidget


class QdockwidgetFootnote(Qdockwidget):
    def __init__(self, *args, **kwargs):
        super(QdockwidgetFootnote, self).__init__(*args, **kwargs)

        self.qwidgetFootnote.close_view.connect(self.close)
