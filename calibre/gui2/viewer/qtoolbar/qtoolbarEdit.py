from calibre.gui2.viewer.qtoolbar.qtoolbar import Qtoolbar


class QtoolbarEdit(Qtoolbar):
    def __init__(self, parent=None):
        super(QtoolbarEdit, self).__init__(parent)

    def addAction(self, *__args):
        self._addAction(*__args)

    @property
    def mode_global_qaction(self):
        return True

    def _addAction(self, action):
        super(QtoolbarEdit, self)._addAction(action)
        if action.menu():
            data = action.data() or {}
            popup = data.get("popup", None)
            if popup is not None:
                qwidget = self.widgetForAction(action)
                qwidget.setPopupMode(getattr(qwidget, popup))

    def contextMenuEvent(self, ev):
        ac = self.actionAt(ev.pos())
        if ac is None:
            return
        ch = self.widgetForAction(ac)
        sm = getattr(ch, 'showMenu', None)
        if callable(sm):
            ev.accept()
            sm()
