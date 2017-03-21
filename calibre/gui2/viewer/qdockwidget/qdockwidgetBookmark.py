from calibre.gui2.viewer.qdockwidget.qdockwidget import Qdockwidget


class QdockwidgetBookmark(Qdockwidget):
    def __init__(self, *args, **kwargs):
        super(QdockwidgetBookmark, self).__init__(*args, **kwargs)

    @property
    def qwidgettitlebar(self):
        return self.titleBarWidget()
