from PyQt5.QtWidgets import QMenu

from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class Qmenu(QMenu, Qwidget):
    def __init__(self, *args, **kwargs):
        super(Qmenu, self).__init__(*args, **kwargs)

    def __getattribute__(self, name):
        try:
            value = super(Qmenu, self).__getattribute__(name)
        except AttributeError:
            value = getattr(self.parent(), name)

        return value

    def add_qapplication_actions(self, qactions):
        pass

    def exec_(self, *args):
        if self.selected_text:
            qactions = filter(
                lambda qaction: qaction.data().get("context", None) == "text",
                self.qapplication_qactions
            )
            map(self.add_qaction, qactions)

        return super(Qmenu, self).exec_(*args)

    def addActions(self, qactions):
        return list(map(self.add_qaction, qactions))

    def add_qaction(self, qaction):
        # todo use position
        if not qaction.isEnabled():
            return
        try:
            qaction.update()
        except AttributeError:
            pass

        o = super(Qmenu, self).addAction(qaction)
        if getattr(qaction, "separator", None):
            self.addSeparator()

        return o

    def addAction(self, *args, **kwargs):
        try:
            return self.add_qaction(*args, **kwargs)
        except TypeError:
            return super(Qmenu, self).addAction(*args, **kwargs)
