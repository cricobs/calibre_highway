from functools import partial

from PyQt5.Qt import (
    Qt, QKeySequence, QListView, QVBoxLayout, QLabel,
    QHBoxLayout, QWidget, QApplication, QStyledItemDelegate, QStyle, QIcon,
    QTextDocument, QRectF, QFrame, QSize, QFont, QRadioButton, QPushButton, QToolButton
)

from calibre.gui2 import error_dialog
from calibre.gui2.viewer.qwidget.qwidget import Qwidget

DEFAULTS = Qt.UserRole
DESCRIPTION = Qt.UserRole + 1
CUSTOM = Qt.UserRole + 2
KEY = Qt.UserRole + 3

_ = _
I = I


class Customize(QFrame):
    def __init__(self, index, dup_check, parent=None):
        QFrame.__init__(self, parent)
        self.setFrameShape(self.StyledPanel)
        self.setFrameShadow(self.Raised)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setAutoFillBackground(True)
        self.l = l = QVBoxLayout(self)
        self.header = la = QLabel(self)
        la.setWordWrap(True)
        l.addWidget(la)
        self.default_shortcuts = QRadioButton(_("&Default"), self)
        self.custom = QRadioButton(_("&Custom"), self)
        self.custom.toggled.connect(self.custom_toggled)
        l.addWidget(self.default_shortcuts)
        l.addWidget(self.custom)
        for which in 1, 2:
            la = QLabel(_("&Shortcut:") if which == 1 else _("&Alternate shortcut:"))
            setattr(self, 'label%d' % which, la)
            h = QHBoxLayout()
            l.addLayout(h)
            h.setContentsMargins(25, -1, -1, -1)
            h.addWidget(la)
            b = QPushButton(_("Click to change"), self)
            la.setBuddy(b)
            b.clicked.connect(partial(self.capture_clicked, which=which))
            b.installEventFilter(self)
            setattr(self, 'button%d' % which, b)
            h.addWidget(b)
            c = QToolButton(self)
            c.setIcon(QIcon(I('clear_left.png')))
            c.setToolTip(_('Clear'))
            h.addWidget(c)
            c.clicked.connect(partial(self.clear_clicked, which=which))
            setattr(self, 'clear%d' % which, c)
        self.data_model = index.model()
        self.capture = 0
        self.key = None
        self.shorcut1 = self.shortcut2 = None
        self.dup_check = dup_check
        self.custom_toggled(False)

    def eventFilter(self, obj, event):
        if self.capture == 0 or obj not in (self.button1, self.button2):
            return QFrame.eventFilter(self, obj, event)
        t = event.type()
        if t == event.ShortcutOverride:
            event.accept()
            return True
        if t == event.KeyPress:
            self.key_press_event(event, 1 if obj is self.button1 else 2)
            return True
        return QFrame.eventFilter(self, obj, event)

    def clear_button(self, which):
        b = getattr(self, 'button%d' % which)
        s = getattr(self, 'shortcut%d' % which, None)
        b.setText(_('None') if s is None else s.toString(QKeySequence.NativeText))
        b.setFont(QFont())

    def clear_clicked(self, which=0):
        setattr(self, 'shortcut%d' % which, None)
        self.clear_button(which)

    def custom_toggled(self, checked):
        for w in ('1', '2'):
            for o in ('label', 'button', 'clear'):
                getattr(self, o + w).setEnabled(checked)

    def capture_clicked(self, which=1):
        self.capture = which
        for w in 1, 2:
            self.clear_button(w)
        button = getattr(self, 'button%d' % which)
        button.setText(_('Press a key...'))
        button.setFocus(Qt.OtherFocusReason)
        font = QFont()
        font.setBold(True)
        button.setFont(font)

    def key_press_event(self, ev, which=0):
        code = ev.key()
        if self.capture == 0 or code in (0, Qt.Key_unknown,
                                         Qt.Key_Shift, Qt.Key_Control, Qt.Key_Alt, Qt.Key_Meta,
                                         Qt.Key_AltGr, Qt.Key_CapsLock, Qt.Key_NumLock,
                                         Qt.Key_ScrollLock):
            return QWidget.keyPressEvent(self, ev)
        sequence = QKeySequence(code | (int(ev.modifiers()) & ~Qt.KeypadModifier))
        setattr(self, 'shortcut%d' % which, sequence)
        self.clear_button(which)
        self.capture = 0
        dup_desc = self.dup_check(sequence, self.key)
        if dup_desc is not None:
            error_dialog(self, _('Already assigned'),
                         unicode(sequence.toString(QKeySequence.NativeText)) + ' ' +
                         _('already assigned to') + ' ' + dup_desc, show=True)
            self.clear_clicked(which=which)


class Delegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        QStyledItemDelegate.__init__(self, parent)
        self.editing_indices = {}
        self.closeEditor.connect(self.editing_done)

    def to_doc(self, index):
        doc = QTextDocument()
        doc.setHtml(index.data())
        return doc

    def editing_done(self, editor, hint):
        remove = None
        for row, w in self.editing_indices.items():
            remove = (row, w.data_model.index(row))
        if remove is not None:
            self.editing_indices.pop(remove[0])
            self.sizeHintChanged.emit(remove[1])

    def sizeHint(self, option, index):
        if index.row() in self.editing_indices:
            return QSize(200, 200)
        ans = self.to_doc(index).size().toSize()
        ans.setHeight(ans.height() + 10)
        return ans

    def paint(self, painter, option, index):
        painter.save()
        painter.setClipRect(QRectF(option.rect))
        if hasattr(QStyle, 'CE_ItemViewItem'):
            QApplication.style().drawControl(QStyle.CE_ItemViewItem, option, painter)
        elif option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
        painter.translate(option.rect.topLeft())
        self.to_doc(index).drawContents(painter)
        painter.restore()

    def createEditor(self, parent, option, index):
        w = Customize(index, index.model().duplicate_check, parent=parent)
        self.editing_indices[index.row()] = w
        self.sizeHintChanged.emit(index)
        return w

    def setEditorData(self, editor, index):
        defs = index.data(DEFAULTS)
        defs = _(' or ').join([unicode(x.toString(x.NativeText)) for x in defs])
        editor.key = unicode(index.data(KEY))
        editor.default_shortcuts.setText(_('&Default') + ': %s' % defs)
        editor.default_shortcuts.setChecked(True)
        editor.header.setText('<b>%s: %s</b>' % (_('Customize shortcuts for'),
                                                 unicode(index.data(DESCRIPTION))))
        custom = index.data(CUSTOM)
        if custom:
            editor.custom.setChecked(True)
            for x in (0, 1):
                button = getattr(editor, 'button%d' % (x + 1))
                if len(custom) > x:
                    seq = QKeySequence(custom[x])
                    button.setText(seq.toString(seq.NativeText))
                    setattr(editor, 'shortcut%d' % (x + 1), seq)

    def setModelData(self, editor, model, index):
        self.closeEditor.emit(editor, self.NoHint)
        custom = []
        if editor.custom.isChecked():
            for x in ('1', '2'):
                sc = getattr(editor, 'shortcut' + x, None)
                if sc is not None:
                    custom.append(sc)

        model.set_data(index, custom)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class QwidgetShortcut(Qwidget):
    def __init__(self, model, parent=None):
        super(QwidgetShortcut, self).__init__(parent)

        self._layout = QHBoxLayout()
        self.setLayout(self._layout)
        self.view = QListView(self)
        self._layout.addWidget(self.view)
        self.view.setModel(model)
        self.delegate = Delegate()
        self.view.setItemDelegate(self.delegate)
        self.delegate.sizeHintChanged.connect(self.scrollTo,
                                              type=Qt.QueuedConnection)

    def scrollTo(self, index):
        self.view.scrollTo(index, self.view.EnsureVisible)

    @property
    def is_editing(self):
        return self.view.state() == self.view.EditingState
