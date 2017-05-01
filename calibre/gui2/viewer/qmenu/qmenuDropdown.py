from PyQt5.QtWidgets import QMenu


# note not inheriting Qmenu

class QmenuDropdown(QMenu):
    def __init__(self, *args, **kwargs):
        super(QmenuDropdown, self).__init__(*args, **kwargs)

    def addActions(self, qactions):
        map(self._addAction, qactions)

    def _addAction(self, action):
        if not action.isEnabled():
            return

        super(QmenuDropdown, self).addAction(action)
        try:
            if action.separator:
                self.addSeparator()
        except AttributeError:
            pass

    def addAction(self, *args, **kwargs):
        try:
            self._addAction(*args, **kwargs)
        except (TypeError, AttributeError):
            super(QmenuDropdown, self).addAction(*args, **kwargs)
