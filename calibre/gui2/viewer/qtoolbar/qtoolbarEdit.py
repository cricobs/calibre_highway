from calibre.gui2.viewer.qtoolbar.qtoolbar import Qtoolbar


class QtoolbarEdit(Qtoolbar):
    def __init__(self, parent=None):
        super(QtoolbarEdit, self).__init__(parent)

        self.qapplication.qactionAdded.connect(self.on_qapplication_qactionAdded)

    def on_qapplication_qactionAdded(self, parent, qaction):
        if qaction in self.actions():
            return

        parents = getattr(qaction, "parents", [])
        if self.__class__.__name__ not in parents:
            return

        # self.qapplication.blockSignals(True)
        self.addAction(qaction)
        if qaction.menu():
            data = qaction.data()
            if data:
                popup = data.get("popup", None)
                if popup:
                    qwidget = self.widgetForAction(qaction)
                    qwidget.setPopupMode(getattr(qwidget, popup))

        # self.qapplication.blockSignals(False)

    def addAction(self, qaction):
        r = super(QtoolbarEdit, self).addAction(qaction)
        if getattr(qaction, "separator", None):
            self.addSeparator()

        return r

    def contextMenuEvent(self, ev):
        ac = self.actionAt(ev.pos())
        if ac is None:
            return
        ch = self.widgetForAction(ac)
        sm = getattr(ch, 'showMenu', None)
        if callable(sm):
            ev.accept()
            sm()
