from calibre.gui2.viewer.qdockwidget.qdockwidget import Qdockwidget
from calibre.gui2.viewer.qwidget.qwidgetSearchReplace import QwidgetSearchReplace


class QdockwidgetSynopsis(Qdockwidget):
    def __init__(self, *args, **kwargs):
        super(QdockwidgetSynopsis, self).__init__(*args, **kwargs)

        self.qwidgetSearchReplace = QwidgetSearchReplace(self)
