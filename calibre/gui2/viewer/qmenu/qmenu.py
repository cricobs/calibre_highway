from PyQt5.QtWidgets import QMenu

from calibre.gui2.viewer.qaction.qaction import Qaction
from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class Qmenu(QMenu, Qwidget):
    def __init__(self, *args, **kwargs):
        super(Qmenu, self).__init__(*args, **kwargs)

    def exec_(self, *args):
        # todo add qactions
        """
        filter(
            lambda qaction: qaction.data().get("selected_text", None),
            self.qapplication.qactions[qmenu.__class__.__name__]
        )
        """
        print (getattr(self.parent(), "selected_text", None))
        return super(Qmenu, self).exec_(*args)

    def addActions(self, qactions):
        return list(map(self._addAction, qactions))

    def _addAction(self, qaction):
        o = super(Qmenu, self).addAction(qaction)
        if getattr(qaction, "separator", True):
            self.addSeparator()

        return o

    def addAction(self, *args, **kwargs):
        try:
            return self._addAction(*args, **kwargs)
        except TypeError:
            return super(Qmenu, self).addAction(*args, **kwargs)
