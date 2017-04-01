from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal

from calibre.gui2 import config
from calibre.gui2.viewer.qcombobox.qcombobox import Qcombobox
from calibre.gui2.viewer.qlineedit.qlineeditSearch import QlineeditSearch

_ = _
I = I


class AsYouType(unicode):
    def __new__(cls, text):
        self = unicode.__new__(cls, text)
        self.as_you_type = True
        return self


class QcomboboxSearch(Qcombobox):  # {{{

    '''
    To use this class:

        * Call initialize()
        * Connect to the search() and cleared() signals from this widget.
        * Connect to the changed() signal to know when the box content changes
        * Connect to focus_to_library() signal to be told to manually change focus
        * Call search_done() after every search is complete
        * Call set_search_string() to perform a search programmatically
        * You can use the current_text property to get the current search text
          Be aware that if you are using it in a slot connected to the
          changed() signal, if the connection is not queued it will not be
          accurate.
    '''

    INTERVAL = 1500  #: Time to wait before emitting search signal
    MAX_COUNT = 25

    search = pyqtSignal(object)
    cleared = pyqtSignal()
    changed = pyqtSignal()
    focus_to_library = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(QcomboboxSearch, self).__init__(*args, **kwargs)

        self.normal_background = 'rgb(255, 255, 255, 0%)'
        self.line_edit = QlineeditSearch(self)
        self.setLineEdit(self.line_edit)

        c = self.line_edit.completer()
        c.setCompletionMode(c.PopupCompletion)
        c.highlighted[str].connect(self.completer_used)

        self.line_edit.key_pressed.connect(self.key_pressed, type=Qt.DirectConnection)
        # QueuedConnection as workaround for https://bugreports.qt-project.org/browse/QTBUG-40807
        self.activated[str].connect(self.history_selected, type=Qt.QueuedConnection)
        self.setEditable(True)
        self.as_you_type = True
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.timer_event, type=Qt.QueuedConnection)
        self.setInsertPolicy(self.NoInsert)
        self.setMaxCount(self.MAX_COUNT)
        self.setSizeAdjustPolicy(self.AdjustToMinimumContentsLengthWithIcon)
        self.setMinimumContentsLength(25)
        self._in_a_search = False
        self.tool_tip_text = self.toolTip()

    def initialize(self, opt_name, colorize=False, help_text=_('Search')):
        self.as_you_type = config['search_as_you_type']
        self.opt_name = opt_name
        items = []
        for item in config[opt_name]:
            if item not in items:
                items.append(item)
        self.addItems(items)
        self.line_edit.setPlaceholderText(help_text)
        self.colorize = colorize
        self.clear()

    def hide_completer_popup(self):
        try:
            self.lineEdit().completer().popup().setVisible(False)
        except:
            pass

    def normalize_state(self):
        self.setToolTip(self.tool_tip_text)
        self.line_edit.setStyleSheet(
            'QLineEdit{color:none;background-color:%s;}' % self.normal_background)

    def text(self):
        return self.currentText()

    def clear_history(self, *args):
        self.clear()

    def clear(self, emit_search=True):
        self.normalize_state()
        self.setEditText('')
        if emit_search:
            self.search.emit('')
        self._in_a_search = False
        self.cleared.emit()

    def clear_clicked(self, *args):
        self.clear()

    def search_done(self, ok):
        if isinstance(ok, basestring):
            self.setToolTip(ok)
            ok = False
        if not unicode(self.currentText()).strip():
            self.clear(emit_search=False)
            return
        self._in_a_search = ok
        col = 'rgba(0,255,0,20%)' if ok else 'rgb(255,0,0,20%)'
        if not self.colorize:
            col = self.normal_background
        self.line_edit.setStyleSheet('QLineEdit{color:black;background-color:%s;}' % col)

    # Comes from the lineEdit control
    def key_pressed(self, event):
        k = event.key()
        if k in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down,
                 Qt.Key_Home, Qt.Key_End, Qt.Key_PageUp, Qt.Key_PageDown,
                 Qt.Key_unknown):
            return
        self.normalize_state()
        if self._in_a_search:
            self.changed.emit()
            self._in_a_search = False
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.do_search()
            self.focus_to_library.emit()
        elif self.as_you_type and unicode(event.text()):
            self.timer.start(1500)

    # Comes from the combobox itself
    def keyPressEvent(self, event):
        k = event.key()
        if k in (Qt.Key_Enter, Qt.Key_Return):
            return self.do_search()
        elif k in (Qt.Key_Escape,):
            self.parent().keyPressEvent(event)
        if k not in (Qt.Key_Up, Qt.Key_Down):
            super(QcomboboxSearch, self).keyPressEvent(event)
        else:
            self.blockSignals(True)
            self.normalize_state()
            super(QcomboboxSearch, self).keyPressEvent(event)
            self.blockSignals(False)

    def completer_used(self, text):
        self.timer.stop()
        self.normalize_state()

    def timer_event(self):
        self._do_search(as_you_type=True)

    def history_selected(self, text):
        self.changed.emit()
        self.do_search()

    def _do_search(self, store_in_history=True, as_you_type=False):
        self.hide_completer_popup()
        text = unicode(self.currentText()).strip()
        if not text:
            return self.clear()
        if as_you_type:
            text = AsYouType(text)
        self.search.emit(text)

        if store_in_history:
            idx = self.findText(text, Qt.MatchFixedString | Qt.MatchCaseSensitive)
            self.block_signals(True)
            if idx < 0:
                self.insertItem(0, text)
            else:
                t = self.itemText(idx)
                self.removeItem(idx)
                self.insertItem(0, t)
            self.setCurrentIndex(0)
            self.block_signals(False)
            history = [unicode(self.itemText(i)) for i in
                       range(self.count())]
            config[self.opt_name] = history

    def do_search(self, *args):
        self._do_search()

    def block_signals(self, yes):
        self.blockSignals(yes)
        self.line_edit.blockSignals(yes)

    def set_search_string(self, txt, store_in_history=False, emit_changed=True):
        if not store_in_history:
            self.activated[str].disconnect()
        try:
            self.setFocus(Qt.OtherFocusReason)
            if not txt:
                self.clear()
            else:
                self.normalize_state()
                # must turn on case sensitivity here so that tag browser strings
                # are not case-insensitively replaced from history
                self.line_edit.completer().setCaseSensitivity(Qt.CaseSensitive)
                self.setEditText(txt)
                self.line_edit.end(False)
                if emit_changed:
                    self.changed.emit()
                self._do_search(store_in_history=store_in_history)
                self.line_edit.completer().setCaseSensitivity(Qt.CaseInsensitive)
            self.focus_to_library.emit()
        finally:
            if not store_in_history:
                # QueuedConnection as workaround for https://bugreports.qt-project.org/browse/QTBUG-40807
                self.activated[str].connect(self.history_selected, type=Qt.QueuedConnection)

    def search_as_you_type(self, enabled):
        self.as_you_type = enabled

    def in_a_search(self):
        return self._in_a_search

    def set_text(self, text):
        if not text:
            return

        self.lineEdit().setText(text)

    @property
    def current_text(self):
        return unicode(self.lineEdit().text())
