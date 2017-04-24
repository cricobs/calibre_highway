import json
from PyQt5.uic import loadUi

from PyQt5.QtCore import QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from calibre.gui2.viewer.library.filepath import filepath_relative
from calibre.gui2.viewer.qaction.qaction import Qaction

I = I


class Qobject(QObject, object):
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
            if group:  # allow group to be specified within the action
                self.create_action(qmenu=qmenu, group=group, **options)
            else:
                self.create_action(qmenu=qmenu, **options)

    def create_action(self, name, text=None, slots=None, icon=None, checkable=False,
                      separator=False, qmenu=None, enabled=True, data=None,
                      actions=None, parents=None, signals=None, group=None, action=None,
                      dropdown=None):

        if group and not qmenu:
            n = "qmenu_" + group
            try:
                qmenu = getattr(self, n)
            except AttributeError:
                # lookout if isinstance(self, Qmenu)
                from calibre.gui2.viewer.qmenu.qmenu import Qmenu

                qmenu = Qmenu(self)
                setattr(self, n, qmenu)

        text = text or name
        if action:
            qaction = reduce(getattr, action, self)
        elif qmenu:
            qaction = Qaction(text, qmenu)
            qmenu.addAction(qaction)
        else:
            qaction = Qaction(text, self)

        qaction.setCheckable(checkable)
        qaction.setObjectName('qaction_' + name.replace(" ", "_").lower())
        qaction.setEnabled(enabled)
        qaction.setData(data or {})
        qaction.setIcon(QIcon(I(icon)))
        qaction.parents = parents or []
        qaction.separator = separator
        qaction.group = group

        if group:
            group_actions = []
            n = group + "_qactions"
            try:
                group_actions = getattr(self, n)
            except AttributeError:
                setattr(self, n, group_actions)
            finally:
                group_actions.append(qaction)
        if slots:
            for signal, names in slots.items():
                slot = reduce(getattr, names, self)
                getattr(qaction, signal).connect(slot)
        if signals:
            for slot, names in signals.items():
                signal = reduce(getattr, names, self)
                signal.connect(getattr(qaction, slot))
        if dropdown:
            setattr(self, 'qmenu_' + dropdown, qaction.create_qmenu())
        if actions:
            self.create_actions(actions, qaction.create_qmenu())

        self.addAction(qaction)

        return qaction

    def add_qapplication_actions(self, qactions):
        for qaction in qactions:
            self.add_qapplication_action(qaction)

    def add_qapplication_action(self, qaction):
        # self.qapplication.blockSignals(True)
        self.addAction(qaction)
        # self.qapplication.blockSignals(False)
