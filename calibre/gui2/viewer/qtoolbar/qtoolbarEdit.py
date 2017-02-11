from calibre.gui2.viewer.qtoolbar.qtoolbar import Qtoolbar


class QtoolbarEdit(Qtoolbar):
    def contextMenuEvent(self, ev):
        ac = self.actionAt(ev.pos())
        if ac is None:
            return
        ch = self.widgetForAction(ac)
        sm = getattr(ch, 'showMenu', None)
        if callable(sm):
            ev.accept()
            sm()
