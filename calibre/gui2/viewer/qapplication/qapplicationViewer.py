from calibre.gui2.viewer.qapplication.qapplication import Qapplication
from calibre.gui2.viewer.qwidget.qwidgetSearchReplace import QwidgetSearchReplace


class QapplicationViewer(Qapplication):
    def __init__(self, *args, **kwargs):
        super(QapplicationViewer, self).__init__(*args, **kwargs)

        self.qwidgetSearchReplace = QwidgetSearchReplace()
