from calibre.gui2.viewer.qwebview.qwebview import Qwebview


class QwebviewFootnote(Qwebview):
    def __init__(self, *args, **kwargs):
        super(QwebviewFootnote, self).__init__(*args, **kwargs)

    def contextMenuEvent(self, qevent):
        menu = self.page().createStandardContextMenu()
        if not menu.exec_(qevent.globalPos()):
            super(QwebviewFootnote, self).contextMenuEvent(qevent)
