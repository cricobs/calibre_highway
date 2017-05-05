from calibre.gui2.viewer.qtoolbar.qtoolbar import Qtoolbar


class QtoolbarSynopsis(Qtoolbar):
    def __init__(self, parent=None):
        super(QtoolbarSynopsis, self).__init__(parent)

        self.visible_qactions = set()

    def _addAction(self, action):
        super(QtoolbarSynopsis, self)._addAction(action)

        action.visibilityChanged.connect(self.on_action_visibilityChanged)

    def on_action_visibilityChanged(self):
        qaction = self.sender()
        if qaction.visible:
            self.visible_qactions.add(qaction)
        else:
            try:
                self.visible_qactions.remove(qaction)
            except KeyError:
                pass

        self.setVisible(not bool(self.visible_qactions))
