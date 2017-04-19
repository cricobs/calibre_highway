from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtGui import QKeySequence

from calibre.gui2.viewer.qabstractlistmodel.qabstractlistmodel import Qabstractlistmodel
from calibre.utils.config import XMLConfig
from calibre.utils.icu import sort_key

DEFAULTS = Qt.UserRole
DESCRIPTION = Qt.UserRole + 1
CUSTOM = Qt.UserRole + 2
KEY = Qt.UserRole + 3

_ = _
I = I


class QabstractlistmodelShortcut(Qabstractlistmodel):
    TEMPLATE = u'''
    <p><b>{0}</b><br>
    {2}: <code>{1}</code></p>
    '''

    def __init__(self, shortcuts, config_file_base_name, parent=None):
        def __init__(self, *args, **kwargs):
            super(QabstractlistmodelShortcut, self).__init__(*args, **kwargs)

        self.descriptions = {}
        for k, v in shortcuts.items():
            self.descriptions[k] = v[-1]
        self.keys = {}
        for k, v in shortcuts.items():
            self.keys[k] = v[0]
        self.order = list(shortcuts)
        self.order.sort(key=lambda x: sort_key(self.descriptions[x]))
        self.sequences = {}
        for k, v in self.keys.items():
            self.sequences[k] = [QKeySequence(x) for x in v]

        self.custom = XMLConfig(config_file_base_name)

    def rowCount(self, parent):
        return len(self.order)

    def get_sequences(self, key):
        custom = self.custom.get(key, [])
        if custom:
            return [QKeySequence(x) for x in custom]
        return self.sequences.get(key, [])

    def get_match(self, event_or_sequence, ignore=tuple()):
        q = event_or_sequence
        if isinstance(q, QKeyEvent):
            q = QKeySequence(q.key() | (int(q.modifiers()) & ~Qt.KeypadModifier))
        for key in self.order:
            if key not in ignore:
                for seq in self.get_sequences(key):
                    if seq.matches(q) == QKeySequence.ExactMatch:
                        return key
        return None

    def duplicate_check(self, seq, ignore):
        key = self.get_match(seq, ignore=[ignore])
        if key is not None:
            return self.descriptions[key]

    def get_shortcuts(self, key):
        return [unicode(x.toString(x.NativeText)) for x in
                self.get_sequences(key)]

    def data(self, index, role):
        row = index.row()
        if row < 0 or row >= len(self.order):
            return None
        key = self.order[row]
        if role == Qt.DisplayRole:
            return self.TEMPLATE.format(self.descriptions[key],
                                        _(' or ').join(self.get_shortcuts(key)), _('Keys'))
        if role == Qt.ToolTipRole:
            return _('Double click to change')
        if role == DEFAULTS:
            return self.sequences[key]
        if role == DESCRIPTION:
            return self.descriptions[key]
        if role == CUSTOM:
            if key in self.custom:
                return self.custom[key]
            else:
                return []
        if role == KEY:
            return key
        return None

    def set_data(self, index, custom):
        key = self.order[index.row()]
        if custom:
            self.custom[key] = [unicode(x.toString(QKeySequence.PortableText)) for x in custom]
        elif key in self.custom:
            del self.custom[key]

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return super(QabstractlistmodelShortcut, self).flags(index) | Qt.ItemIsEditable
