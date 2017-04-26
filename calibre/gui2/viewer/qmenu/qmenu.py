from PyQt5.QtWidgets import QMenu

from calibre.gui2.viewer.qwidget.qwidget import Qwidget


def actions_sorter(action):
    try:
        position = action.data().get("position", None)
    except AttributeError:
        position = None

    return position is None, position


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
        actions = self.actions()
        if self.selected_text:
            actions += filter(
                lambda q: q.data().get("context", None) == "text", self.qapplication_qactions)

        for action in sorted(actions, key=actions_sorter):
            self._addAction(action)
            if getattr(action, "separator", None):
                self.addSeparator()

        return super(Qmenu, self).exec_(*args)

    def addActions(self, qactions):
        map(self._addAction, qactions)

    def _addAction(self, action):
        """
        reimplementation of addAction(action)
        :param action:
        :return:
        """
        if not action.isEnabled():
            return
        try:
            action.update()
        except AttributeError:
            pass

        super(Qmenu, self).addAction(action)

    def addAction(self, *args, **kwargs):
        try:
            self._addAction(*args, **kwargs)
        except TypeError:
            super(Qmenu, self).addAction(*args, **kwargs)
