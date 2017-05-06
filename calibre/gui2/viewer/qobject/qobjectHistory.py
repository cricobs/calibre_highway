from PyQt5.QtCore import pyqtSignal

from calibre.gui2.viewer.qobject.qobject import Qobject


class ListHistory(list):
    def __init__(self, manager):
        super(ListHistory, self).__init__(self)

        self.manager = manager
        self.clear()

    def clear(self):
        del self[:]
        self.p_insert = 0
        self.p_back = None
        self.p_forward = None
        self.update_actions()

    def update_actions(self):
        self.manager(self.p_back is None, self.p_forward is None)

    def back(self, position_when_clicked):
        if self.p_back is None:
            return None

        position = self[self.p_back]
        self.p_forward = self.p_back + 1
        if self.p_forward >= len(self):
            # We are at the head of the stack, append position to the stack so that
            # clicking forward again will take us to where we were when we
            # clicked back
            self.append(position_when_clicked)
            self.p_forward = len(self) - 1

        self.p_insert = self.p_forward
        self.p_back = None if self.p_back == 0 else self.p_back - 1

        self.update_actions()

        return position

    def forward(self, position_when_clicked):
        if self.p_forward is None:
            return None

        position = self[self.p_forward]
        self.p_back = self.p_forward - 1
        if self.p_back < 0:
            self.p_back = None

        self.p_insert = min(len(self) - 1, (self.p_back or 0) + 1)
        self.p_forward = None if self.p_forward > len(self) - 2 else self.p_forward + 1

        self.update_actions()

        return position

    def add(self, position):
        # Link clicked
        self[self.p_insert:] = []
        while self.p_insert > 0 and self[self.p_insert - 1] == position:
            self.p_insert -= 1
            self[self.p_insert:] = []

        self.insert(self.p_insert, position)

        self.p_back = self.p_insert  # The next back must go to position
        self.p_insert += 1
        self.p_forward = None  # There can be no forward

        self.update_actions()

    def __str__(self):
        return 'History: Items=%s back_pos=%s insert_pos=%s forward_pos=%s' % (
            tuple(self), self.p_back, self.p_insert, self.p_forward)


class QobjectHistory(Qobject):
    goToPosition = pyqtSignal(int)

    def __init__(self, parent=None, *args, **kwargs):
        super(QobjectHistory, self).__init__(parent, *args, **kwargs)

        self.position = None
        self.listHistory = ListHistory(self.update_qactions)

        self.set_manager(parent)

    def set_manager(self, manager):
        try:
            manager.iteratorExited.connect(self.on_manager_iteratorExited)
            manager.positionChanged.connect(self.on_manager_positionChanged)
        except AttributeError:
            pass

    def on_manager_positionChanged(self, position, store):
        self.position = position
        if store:
            self.listHistory.add(position)

    def on_manager_iteratorExited(self):
        self.clear()

    def update_qactions(self, back, forward):
        self.qaction_back.setDisabled(back)
        self.qaction_forward.setDisabled(forward)

    def clear(self):
        self.listHistory.clear()

    def back(self, *args, **kwargs):
        self.go_to_position(self.listHistory.back(self.position))

    def forward(self, *args, **kwargs):
        self.go_to_position(self.listHistory.forward(self.position))

    def go_to_position(self, position):
        if position:
            self.goToPosition.emit(position)

    def add(self, *args, **kwargs):
        self.listHistory.add(*args, **kwargs)

    def addAction(self, qaction):
        setattr(self, qaction.objectName(), qaction)

        self.parent().addAction(qaction)
