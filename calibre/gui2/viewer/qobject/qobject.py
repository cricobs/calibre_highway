import json
from PyQt5.uic import loadUi

from PyQt5.QtCore import QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMenu

from calibre.gui2.viewer.qaction.qaction import Qaction
from calibre.library.filepath import filepath_relative


class Qobject(QObject):
    def __init__(self, *args, **kwargs):
        super(Qobject, self).__init__(*args, **kwargs)

        self._options = None

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
                self.options = json.load(iput)

        # fixme
        """
        connect self.qapplication.qactionAdded to self.add_qapplication_action with
        self.__class__.__name__ argument?
        """
        qactions = self.qapplication.qactions.get(self.__class__.__name__)
        if qactions:
            self.add_qapplication_actions(qactions)

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, options):
        self._options = options

        if self._options:
            self.load_options(self._options)

    def load_options(self, options):
        actions = options.get("actions", None)
        if actions:
            self.create_actions(actions)

    def create_actions(self, actions, qmenu=None):
        try:
            for group, _actions in actions.items():
                self._create_actions(_actions, qmenu=qmenu, group=group)

        except AttributeError:
            self._create_actions(actions, qmenu=qmenu)

    def _create_actions(self, actions, qmenu=None, group=None):
        for options in actions:
            self.create_action(qmenu=qmenu, group=group, **options)

    def create_action(self, name, text=None, slots=None, icon=None, checkable=False,
                      shortcuts=None, separator=False, qmenu=None, enabled=True, data=None,
                      actions=None, parents=None, signals=None, group=None, *args, **kwargs):
        text = text if text else name

        if group and not qmenu:
            # fixme check if qmenu == True and create qmenu
            qmenu = getattr(self, "qmenu_" + group, None)

        qaction = qmenu.addAction(text) if qmenu else Qaction(text, self)
        qaction.setCheckable(checkable)
        qaction.setObjectName('qaction_' + name)
        qaction.setEnabled(enabled)
        qaction.setData(data)
        qaction.name = name  # fixme use qaction.objectName()

        try:
            qaction.setIcon(icon)
        except TypeError:  # fixme if qaction is created from qmenu
            qaction.setIcon(QIcon(I(icon)))

        group_actions = None
        if group:
            # fixme not well written
            name_group = group + "_qactions"
            group_actions = getattr(self, name_group, [])
            group_actions.append(qaction)

            setattr(self, name_group, group_actions)
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
            # fixme create proper shorcuts manager
            if shortcuts:
                try:
                    sequences = list(map(lambda s: self.shortcuts.get_sequences(s)[0], shortcuts))
                except:
                    qaction.setShortcuts(list(map(QKeySequence, shortcuts)))
                else:
                    data = qaction.data() or {}
                    data["shortcuts"] = " | ".join(shortcuts)

                    qaction.setData(data)
                    qaction.setShortcuts(sequences)
        if separator:
            if qmenu:
                qmenu.addSeparator()
            if group_actions:
                action_separator = Qaction(self)
                action_separator.setSeparator(True)

                group_actions.append(action_separator)
        if actions:
            q = QMenu(self)
            qaction.setMenu(q)
            self.create_actions(actions, q)

        self.addAction(qaction)

        return qaction

    def add_qapplication_actions(self, qactions):
        for qaction in qactions:
            self.add_qapplication_action(qaction)

    def add_qapplication_action(self, qaction):
        self.addAction(qaction)
