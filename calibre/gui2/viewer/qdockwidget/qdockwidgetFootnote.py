from calibre.gui2.viewer.qdockwidget.qdockwidget import Qdockwidget


class QdockwidgetFootnote(Qdockwidget):
    def __init__(self, *args, **kwargs):
        super(QdockwidgetFootnote, self).__init__(*args, **kwargs)

    @property
    def is_auto_hide(self):
        return True
