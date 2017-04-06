import json
from PyQt5.uic import loadUi

from PyQt5.QtCore import QObject
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMenu

from calibre.gui2.viewer.qaction.qaction import Qaction
from calibre.library.filepath import filepath_relative


class Qobject(QObject):
    def __init__(self, *args, **kwargs):
        super(Qobject, self).__init__(*args, **kwargs)

        self._settings = None

        self.qapplication = QApplication.instance()

        ui_path = filepath_relative(self, "ui")
        try:
            loadUi(ui_path, self)
        except IOError as e:
            if e.errno != 2:
                raise

        json_path = filepath_relative(self, "json")
        try:
            iput = open(json_path)
        except IOError as e:
            if e.errno != 2:
                raise
        else:
            with iput:
                self.settings = json.load(iput)

        qactions = self.qapplication.qactions.get(self.__class__.__name__)
        if qactions:
            self.add_qapplication_actions(qactions)

    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, settings):
        self._settings = settings

        if self._settings:
            self.load_settings(self._settings)

    def load_settings(self, settings):
        actions = settings.get("actions", None)
        if actions:
            self.create_actions(actions)

    def create_actions(self, actions, qmenu=None):
        for options in actions:
            self.create_action(qmenu=qmenu, **options)

    def create_action(self, name, text=None, slots=None, icon=None, checkable=False,
                      shortcuts=None,
                      separator=False, qmenu=None, enabled=True, data=None, actions=None,
                      parents=None, signals=None, *args,
                      **kwargs):
        text = text if text else name

        qaction = Qaction(text, self)
        qaction.setCheckable(checkable)
        qaction.setIcon(icon)
        qaction.setObjectName('qaction_' + name)
        qaction.setEnabled(enabled)
        qaction.setData(data)

        if slots:
            for signal, names in slots.items():
                slot = reduce(getattr, names, self)
                getattr(qaction, signal).connect(slot)
        if signals:
            for signal, names in signals.items():
                slot = reduce(getattr, names, qaction)
                getattr(self, signal).connect(slot)
        if parents:
            qaction.parents = parents
        if shortcuts:
            qaction.setShortcuts(list(map(QKeySequence, shortcuts)))
        if qmenu is not None:
            pass
            # qmenu.addAction(qaction)
        if separator:
            pass
            # if qmenu is None:
            #     qaction.setSeparator(True)
            # else:
            #     qmenu.addSeparator()
        if actions:
            q = QMenu(self)
            qaction.setMenu(q)
            self.create_actions(actions, q)

        self.addAction(qaction)

    def add_qapplication_actions(self, qactions):
        for qaction in qactions:
            self.add_qapplication_action(qaction)

    def add_qapplication_action(self, qaction):
        self.addAction(qaction)
