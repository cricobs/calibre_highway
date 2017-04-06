from __future__ import (unicode_literals, division, absolute_import, print_function)

import json
import sys
import zipfile
from collections import OrderedDict

from PyQt5.Qt import (QFont, QDialog, Qt, QColor, QColorDialog, QMenu, QInputDialog,
                      QListWidgetItem, QFormLayout, QLabel, QLineEdit, QDialogButtonBox)
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QAbstractButton
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QDoubleSpinBox
from PyQt5.QtWidgets import QFontComboBox
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QWidget

from calibre.constants import iswindows, isxp
from calibre.gui2 import min_available_height, error_dialog
from calibre.gui2.languages import LanguagesEdit
from calibre.gui2.shortcuts import ShortcutConfig
from calibre.gui2.viewer.qdialog.qdialog import Qdialog
from calibre.library.filepath import filepath_relative
from calibre.utils.config import Config, StringConfig, JSONConfig
from calibre.utils.icu import sort_key
from calibre.utils.localization import get_language, calibre_langcode_to_name

__license__ = 'GPL v3'
__copyright__ = '2012, Kovid Goyal <kovid at kovidgoyal.net>'
__docformat__ = 'restructuredtext en'

"""
To add config [option]:
    - add widget to ui file with objectname [option] | add property with name [option]
    - add config item to json file with key [option]
"""

_ = _;
I = I;
P = P;
dynamic_property = dynamic_property


def config(defaults=None):
    desc = _('Options to customize the ebook viewer')
    if defaults is None:
        c = Config('viewer', desc)
    else:
        c = StringConfig(defaults, desc)

    def add_option(name, default=None, group=None, groups=None, description=None, system=None,
                   **values):
        if group:
            try:
                c.add_group(name, description)
            except ValueError:
                c.groups[name] = description
            return
        elif groups:
            try:
                c.add_group(groups[0], "")
            except ValueError:
                pass
            values["group"] = groups[0]
        if system:
            default = default[0] if iswindows else default[1]

        c.add_opt(name, default=default, **values)

    with open(filepath_relative(sys.modules[__name__], "json"), "r") as iput:
        for name, values in json.load(iput)["config"].items():
            add_option(name, **values)

    oparse = c.parse

    def parse():
        ans = oparse()
        if not ans.cols_per_screen_migrated:
            ans.cols_per_screen_portrait = ans.cols_per_screen_landscape = ans.cols_per_screen
        return ans

    c.parse = parse

    return c


def load_themes():
    return JSONConfig('viewer_themes')


class QdialogConfig(Qdialog):
    def __init__(self, shortcuts, *args, **kwargs):
        super(QdialogConfig, self).__init__(*args, **kwargs)

        self.cols_per_screen = None
        self.cols_per_screen_migrated = None
        self.background_color = None
        self.text_color = None

        self.shortcuts = shortcuts
        self.shortcut_config = ShortcutConfig(shortcuts, parent=self)

        path = P('viewer/hyphenate/patterns.zip', allow_user_override=False)
        with zipfile.ZipFile(path, 'r') as zf:
            pats = [x.split('.')[0].replace('-', '_') for x in zf.namelist()]

        lang_pats = {
            'el_monoton': get_language('el').partition(';')[0] + _(' monotone'),
            'el_polyton': get_language('el').partition(';')[0] + _(' polytone'),
            'sr_cyrl': get_language('sr') + _(' cyrillic'),
            'sr_latn': get_language('sr') + _(' latin'),
        }

        def gl(pat):
            return lang_pats.get(pat, get_language(pat))

        names = list(map(gl, pats))
        pmap = {}
        for i in range(len(pats)):
            pmap[names[i]] = pats[i]
        for x in sorted(names):
            self.hyphenate_default_lang.addItem(x, pmap[x])

        self.hyphenate_pats = pats
        self.hyphenate_names = names

        p = self.tabs.widget(1)
        p.layout().addWidget(self.shortcut_config)

        if isxp:
            self.hyphenate.setVisible(False)
            self.hyphenate_default_lang.setVisible(False)
            self.hyphenate_label.setVisible(False)

        self.themes = load_themes()

        self.load_theme_button.m = m = QMenu()
        self.load_theme_button.setMenu(m)
        m.triggered.connect(self.load_theme)

        self.delete_theme_button.m = m = QMenu()
        self.delete_theme_button.setMenu(m)
        m.triggered.connect(self.delete_theme)

        self.opts = config().parse()
        self.load_options(self.opts)
        self.init_load_themes()
        self.init_dictionaries()

        self.resize(self.width(), min(self.height(), max(575, min_available_height() - 25)))

        for x in 'add remove change'.split():
            getattr(self, x + '_dictionary_website_button').clicked.connect(
                getattr(self, x + '_dictionary_website'))

    @pyqtSlot(bool)
    def on_clear_search_history_button_clicked(self, checked):
        self.clear_search_history()

    @pyqtSlot(bool)
    def on_save_theme_button_clicked(self, checked):
        self.save_theme()

    @pyqtSlot(QAbstractButton)
    def on_buttonBox_clicked(self, qbutton):
        if qbutton == self.buttonBox.RestoreDefaults:
            self.restore_defaults()

    @pyqtSlot(bool)
    def on_change_background_color_button_clicked(self, checked):
        self.change_color("background", reset=False)

    @pyqtSlot(bool)
    def on_change_text_color_button_clicked(self, checked):
        self.change_color("text", reset=False)

    @pyqtSlot(QAbstractButton)
    def on_buttonBox_clicked(self, qabstractbutton):
        if qabstractbutton == self.buttonBox.button(self.buttonBox.RestoreDefaults):
            self.restore_defaults()

    def restore_defaults(self):
        opts = config('').parse()
        self.load_options(opts)

        from calibre.gui2.viewer.qmainwindow.qmainwindowViewer import dprefs, vprefs
        self.word_lookups = dprefs.defaults['word_lookups']
        self.singleinstance.setChecked(vprefs.defaults['singleinstance'])

    def load_options(self, opts):
        methods = {
            QFontComboBox: lambda q, f: q.setCurrentFont(QFont(f)),
            QCheckBox: lambda q, c: q.setChecked(c),
            QSpinBox: lambda q, v: q.setValue(v),
            QDoubleSpinBox: lambda q, v: q.setValue(v),
            QComboBox: lambda q, i: q.setCurrentIndex(i),
            QLineEdit: lambda q, t: q.setText(t or ''),
            QPlainTextEdit: lambda q, t: q.setPlainText(t)
        }

        for name, value in opts.__dict__.items():
            obj = getattr(self, name)
            if not isinstance(obj, QWidget):
                setattr(self, name, value)
            elif obj is self.use_book_margins:
                obj.setChecked(not value)
            elif obj is self.standard_font:
                obj.setCurrentIndex({'serif': 0, 'sans': 1, 'mono': 2}[value])
            elif obj is self.font_magnification_step:
                value = 0.2 if value < 0.01 or value > 1 else value
                obj.setValue(int(value * 100))
            elif obj is self.hyphenate_default_lang:
                try:
                    idx = self.hyphenate_pats.index(value)
                except ValueError:
                    idx = self.hyphenate_pats.index('en_us')

                obj.setCurrentIndex(obj.findText(self.hyphenate_names[idx]))
                obj.setEnabled(opts.hyphenate)
            else:
                for q, method in methods.items():
                    if not isinstance(obj, q):
                        continue
                    try:
                        method(obj, value)
                    except TypeError:
                        pass
                    else:
                        break
                else:
                    raise NotImplementedError(name, value)

        self.update_sample_colors()

        from calibre.gui2.viewer.qmainwindow.qmainwindowViewer import vprefs
        self.singleinstance.setChecked(bool(vprefs['singleinstance']))

    def change_color(self, which, reset=False):
        if reset:
            setattr(self, '%s_color' % which, None)
        else:
            initial = getattr(self, '%s_color' % which)
            if initial:
                initial = QColor(initial)
            else:
                initial = Qt.black if which == 'text' else Qt.white
            title = (_('Choose text color') if which == 'text' else _('Choose background color'))
            col = QColorDialog.getColor(initial, self, title, QColorDialog.ShowAlphaChannel)
            if col.isValid():
                name = unicode(col.name())
                setattr(self, '%s_color' % which, name)

        self.update_sample_colors()

    def update_sample_colors(self):
        for x in ('text', 'background'):
            val = getattr(self, '%s_color' % x)
            if not val:
                val = 'inherit' if x == 'text' else 'transparent'
            ss = 'QLabel { %s: %s }' % ('background-color' if x == 'background' else 'color', val)
            getattr(self, '%s_color_sample' % x).setStyleSheet(ss)

    def clear_search_history(self):
        from calibre.gui2 import config
        config['viewer_search_history'] = []
        config['synopsis_search_history'] = []
        config['viewer_toc_search_history'] = []

    def save_theme(self):
        themename, ok = QInputDialog.getText(self, _('Theme name'),
                                             _('Choose a name for this theme'))
        if not ok:
            return
        themename = unicode(themename).strip()
        if not themename:
            return
        c = config('')
        c.add_opt('theme_name_xxx', default=themename)
        self.save_options(c)
        self.themes['theme_' + themename] = c.src
        self.init_load_themes()
        self.theming_message.setText(_('Saved settings as the theme named: %s') %
                                     themename)

    def init_load_themes(self):
        for x in ('load', 'delete'):
            m = getattr(self, '%s_theme_button' % x).menu()
            m.clear()
            for x in self.themes.iterkeys():
                title = x[len('theme_'):]
                ac = m.addAction(title)
                ac.theme_id = x

    def load_theme(self, ac):
        theme = ac.theme_id
        raw = self.themes[theme]
        self.load_options(config(raw).parse())
        self.theming_message.setText(_('Loaded settings from the theme %s') %
                                     theme[len('theme_'):])

    def delete_theme(self, ac):
        theme = ac.theme_id
        del self.themes[theme]
        self.init_load_themes()
        self.theming_message.setText(_('Deleted the theme named: %s') %
                                     theme[len('theme_'):])

    def init_dictionaries(self):
        from calibre.gui2.viewer.qmainwindow.qmainwindowViewer import dprefs
        self.word_lookups = dprefs['word_lookups']

    @dynamic_property
    def word_lookups(self):
        def fget(self):
            return dict(self.dictionary_list.item(i).data(Qt.UserRole) for i in
                        range(self.dictionary_list.count()))

        def fset(self, wl):
            self.dictionary_list.clear()
            for langcode, url in sorted(wl.iteritems(), key=lambda (lc, url): sort_key(
                    calibre_langcode_to_name(lc))):
                i = QListWidgetItem('%s: %s' % (calibre_langcode_to_name(langcode), url),
                                    self.dictionary_list)
                i.setData(Qt.UserRole, (langcode, url))

        return property(fget=fget, fset=fset)

    def add_dictionary_website(self):
        class AD(QDialog):
            def __init__(self, parent):
                QDialog.__init__(self, parent)
                self.setWindowTitle(_('Add a dictionary website'))
                self.l = l = QFormLayout(self)
                self.la = la = QLabel('<p>' + _(
                    'Choose a language and enter the website address (URL) for it below.'
                    ' The URL must have the placeholder <b>%s</b> in it, '
                    'which will be replaced by the actual word being looked up') % '{word}')
                la.setWordWrap(True)
                l.addRow(la)
                self.le = LanguagesEdit(self)
                l.addRow(_('&Language:'), self.le)
                self.url = u = QLineEdit(self)
                u.setMinimumWidth(350)
                u.setPlaceholderText(_('For example: %s') % 'http://dictionary.com/{word}')
                l.addRow(_('&URL:'), u)
                self.bb = bb = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
                l.addRow(bb)
                bb.accepted.connect(self.accept), bb.rejected.connect(self.reject)
                self.resize(self.sizeHint())

            def accept(self):
                if '{word}' not in self.url.text():
                    return error_dialog(self, _('Invalid URL'), _(
                        'The URL {0} does not have the placeholder <b>{1}</b> in it.').format(
                        self.url.text(), '{word}'), show=True)
                QDialog.accept(self)

        d = AD(self)
        if d.exec_() == d.Accepted:
            url = d.url.text()
            if url:
                wl = self.word_lookups
                for lc in d.le.lang_codes:
                    wl[lc] = url
                self.word_lookups = wl

    def remove_dictionary_website(self):
        idx = self.dictionary_list.currentIndex()
        if idx.isValid():
            lc, url = idx.data(Qt.UserRole)
            wl = self.word_lookups
            wl.pop(lc, None)
            self.word_lookups = wl

    def change_dictionary_website(self):
        idx = self.dictionary_list.currentIndex()
        if idx.isValid():
            lc, url = idx.data(Qt.UserRole)
            url, ok = QInputDialog.getText(self, _('Enter new website'), 'URL:', text=url)
            if ok:
                wl = self.word_lookups
                wl[lc] = url
                self.word_lookups = wl

    def accept(self, *args):
        if self.shortcut_config.is_editing:
            from calibre.gui2 import info_dialog
            info_dialog(self, _('Still editing'), _(
                'You are in the middle of editing a keyboard shortcut first complete that,'
                ' by clicking outside the shortcut editing box.'), show=True)
            return
        self.save_options(config())

        return QDialog.accept(self, *args)

    def save_options(self, c):
        methods = OrderedDict([
            (QFontComboBox, lambda q: unicode(q.currentFont().family())),
            (QCheckBox, lambda q: q.isChecked()),
            (QDoubleSpinBox, lambda q: q.value()),
            (QSpinBox, lambda q: int(q.value())),
            (QComboBox, lambda q: q.currentIndex()),
            (QLineEdit, lambda q: unicode(q.text().strip())),
            (QPlainTextEdit, lambda q: unicode(q.toPlainText()))
        ])

        self.cols_per_screen_migrated = True

        for name in self.opts.__dict__.keys():
            obj = getattr(self, name)
            if not isinstance(obj, QWidget):
                value = obj
            elif obj is self.standard_font:
                value = {0: 'serif', 1: 'sans', 2: 'mono'}[obj.currentIndex()]
            elif obj is self.max_fs_height:
                value = obj.value() if obj.value() <= self.max_fs_height.minimum() else -1
            elif obj is self.font_magnification_step:
                value = float(obj.value()) / 100.
            elif obj is self.hyphenate_default_lang:
                value = obj.itemData(obj.currentIndex())
            elif obj is self.use_book_margins:
                value = not obj.isChecked()
            else:
                for q, method in methods.items():
                    if not isinstance(obj, q):
                        continue
                    try:
                        value = method(obj)
                    except TypeError:
                        pass
                    else:
                        break
                else:
                    raise NotImplementedError(name)

            c.set(name, value)

        from calibre.gui2.viewer.qmainwindow.qmainwindowViewer import dprefs, vprefs
        dprefs['word_lookups'] = self.word_lookups
        vprefs['singleinstance'] = self.singleinstance.isChecked()
