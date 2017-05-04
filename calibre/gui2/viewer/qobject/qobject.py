import json
from PyQt5.uic import loadUi

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtWrapperType
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from calibre.gui2.viewer.library.filepath import filepath_relative
from calibre.gui2.viewer.library.thing import property_setter
from calibre.gui2.viewer.qaction.qaction import Qaction

I = I


class pyqtwrappertype(pyqtWrapperType):
    pass


class Qobject(QObject, object):
    __metaclass__ = pyqtwrappertype

    def __init__(self, *args, **kwargs):
        super(Qobject, self).__init__(*args, **kwargs)

        self.qapplication = QApplication.instance()
        if self.mode_global_qaction:
            self.qapplication.qactionAdded.connect(self.on_qapplication_qactionAdded)
            self.add_qapplication_actions(self.qapplication_qactions)
        if self.mode_activity:
            self.qapplication.inactivityTimeout.connect(self.on_qapplication_inactivityTimeout)
            self.qapplication.activity.connect(self.on_qapplication_activity)

        self.load_ui_file()
        self.load_options_file()

    def on_qapplication_activity(self):
        pass

    def on_qapplication_inactivityTimeout(self, target, interval):
        pass

    @property
    def mode_activity(self):
        """
        connect qapplication.inactivityTimeout to on_qapplication_inactivityTimeout
        connect qapplication.activity to on_qapplication_activity
        :return:
        """
        return False

    def load_ui_file(self):
        ui_path = filepath_relative(self, "ui")
        try:
            loadUi(ui_path, self)
        except IOError as e:
            if e.errno != 2:
                raise
        else:
            self.qapplication.loadedUi.emit(self)

    def load_options_file(self):
        json_path = filepath_relative(self, "json")
        try:
            iput = open(json_path)
        except IOError as e:
            if e.errno != 2:
                raise
        else:
            with iput:
                self.options = json.load(iput)

    @property
    def qapplication_qactions(self):
        return self.qapplication.qactions[self.__class__.__name__]

    def on_qapplication_qactionAdded(self, parent, qaction):
        """
        called if mode_qapplication_qaction
        :param parent:
        :param qaction:
        :return:
        """
        if qaction in self.actions():
            return

        parents = getattr(qaction, "parents", [])
        if self.__class__.__name__ not in parents:
            return

        self.add_qapplication_action(qaction)

    @property
    def mode_global_qaction(self):
        """
        connect qapplication.qactionAdded to on_qapplication_qactionAdded
        addActions(qapplication_qactions)
        :return:
        """
        return False

    @property_setter
    def options(self, options):
        if options:
            self.load_options(options)

    def load_options(self, options=None):
        options = options or self.options
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
            finally:
                qmenu.setObjectName(n)

        text = text or name
        if action:
            qaction = reduce(getattr, action, self)
        else:
            qaction = Qaction(text, qmenu or self)

        qaction.setCheckable(checkable)
        qaction.setObjectName('qaction_' + name.replace(" ", "_").lower())
        qaction.setEnabled(enabled)
        qaction.setData(data)
        qaction.parents = parents or []
        qaction.separator = separator
        qaction.group = group
        if icon:
            qaction.setIcon(QIcon(I(icon)))
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
        if qmenu:
            qmenu.addAction(qaction)

        self.addAction(qaction)

        return qaction

    def add_qapplication_actions(self, qactions):
        for qaction in qactions:
            self.add_qapplication_action(qaction)

    def add_qapplication_action(self, qaction):
        self.qapplication.blockSignals(True)
        self.addAction(qaction)
        self.qapplication.blockSignals(False)
