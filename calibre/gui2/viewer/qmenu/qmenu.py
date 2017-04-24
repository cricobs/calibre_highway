from PyQt5.QtWidgets import QMenu

from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class Qmenu(QMenu, Qwidget):
    def __init__(self, *args, **kwargs):
        super(Qmenu, self).__init__(*args, **kwargs)

    def exec_(self, *args):
        # todo add qactions
        """
        filter(
            lambda qaction: qaction.data().get("group", None),
            self.qapplication.qactions[qmenu.__class__.__name__]
        )
        """
        print (getattr(self.parent(), "selected_text", None))
        return super(Qmenu, self).exec_(*args)
