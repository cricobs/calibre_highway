from calibre.gui2.viewer.qtoolbar.qtoolbar import Qtoolbar


class QtoolbarEdit(Qtoolbar):
    def __init__(self, parent=None):
        super(QtoolbarEdit, self).__init__(parent)

    def addAction(self, *__args):
        self._addAction(*__args)

    @property
    def mode_qapplication_qaction(self):
        return True

    def add_qapplication_action(self, qaction):
        super(QtoolbarEdit, self).add_qapplication_action(qaction)
        if qaction.menu():
            data = qaction.data()
            if data:
                popup = data.get("popup", None)
                if popup:
                    qwidget = self.widgetForAction(qaction)
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
