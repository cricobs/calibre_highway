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
        if self.selected_text:  # note get selected_text via __getattribute__
            actions = filter(
                lambda q: "text" in q.data().get("context", []), self.qapplication_qactions)

            map(self._addAction, actions)

        return super(Qmenu, self).exec_(*args)

    def addActions(self, qactions):
        map(self._addAction, qactions)

    def _addAction(self, action):
        if not action.isEnabled():
            return
        try:
            action.update(qmenu=self, text_format=self.selected_text)
        except AttributeError:
            pass

        super(Qmenu, self)._addAction(action)

    def addAction(self, *args, **kwargs):
        try:
            self._addAction(*args, **kwargs)
        except (TypeError, AttributeError):
            super(Qmenu, self).addAction(*args, **kwargs)
