import json
import os
import sys
import time
import zipfile
from base64 import b64encode

from PyQt5.QtCore import pyqtSignal, Qt, QUrl, pyqtSlot, pyqtProperty, QSize, QPoint, QEventLoop
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWebKit import QWebElement, QWebSettings
from PyQt5.QtWebKitWidgets import QWebPage
from PyQt5.QtWidgets import QDialog, QApplication

import calibre
from calibre import __version__, iswindows, prints
from calibre.constants import isxp, DEBUG
from calibre.customize.ui import all_viewer_plugins
from calibre.gui2.viewer.qdialog.qdialogConfig import QdialogConfig, config
from calibre.gui2.viewer.qnetworkacessmanager.qnetworkaccessmanagerFakeNet import QnetworkaccessmanagerFakeNet
from calibre.library.filepath import filepath_relative
from calibre.utils.localization import lang_as_iso639_1
from calibre.utils.resources import compiled_coffeescript

dynamic_property = dynamic_property


class Document(QWebPage):
    page_turn = pyqtSignal(object)
    mark_element = pyqtSignal(QWebElement)
    settings_changed = pyqtSignal()
    animated_scroll_done_signal = pyqtSignal()

    def __init__(self, shortcuts, parent=None, debug_javascript=False):
        QWebPage.__init__(self, parent)
        self.nam = QnetworkaccessmanagerFakeNet(self)
        self.setNetworkAccessManager(self.nam)
        self.setObjectName("py_bridge")
        self.in_paged_mode = False
        # Use this to pass arbitrary JSON encodable objects between python and
        # javascript. In python get/set the value as: self.bridge_value. In
        # javascript, get/set the value as: py_bridge.value
        self.bridge_value = None
        self.first_load = True
        self.jump_to_cfi_listeners = set()

        self.debug_javascript = debug_javascript
        self.anchor_positions = {}
        self.index_anchors = set()
        self.current_language = None
        self.loaded_javascript = False
        self.js_loader = JavaScriptLoader(dynamic_coffeescript=self.debug_javascript)
        self.in_fullscreen_mode = False
        self.math_present = False

        self.scroll_marks = []
        self.shortcuts = shortcuts
        pal = self.palette()
        pal.setBrush(QPalette.Background, QColor(0xee, 0xee, 0xee))
        self.setPalette(pal)
        self.page_position = PagePosition(self)

        settings = self.settings()

        # Fonts
        self.all_viewer_plugins = tuple(all_viewer_plugins())
        for pl in self.all_viewer_plugins:
            pl.load_fonts()
        opts = config().parse()
        self.set_font_settings(opts)

        apply_basic_settings(settings)
        self.set_user_stylesheet(opts)
        self.misc_config(opts)

        # Load javascript
        self.mainFrame().javaScriptWindowObjectCleared.connect(
            self.add_window_objects)

        self.turn_off_internal_scrollbars()

    def set_font_settings(self, opts):
        settings = self.settings()
        apply_settings(settings, opts)

    def do_config(self, parent=None):
        d = QdialogConfig(self.shortcuts, parent)
        if d.exec_() == QDialog.Accepted:
            opts = config().parse()
            self.apply_settings(opts)

    def apply_settings(self, opts):
        with self.page_position:
            self.set_font_settings(opts)
            self.set_user_stylesheet(opts)
            self.misc_config(opts)
            self.settings_changed.emit()
            self.after_load()

    def turn_off_internal_scrollbars(self):
        mf = self.mainFrame()
        mf.setScrollBarPolicy(Qt.Vertical, Qt.ScrollBarAlwaysOff)
        mf.setScrollBarPolicy(Qt.Horizontal, Qt.ScrollBarAlwaysOff)

    def set_user_stylesheet(self, opts):
        brules = [
            'background-color: %s !important' % opts.background_color] if opts.background_color else [
            'background-color: white']
        prefix = '''
            body { %s  }
        ''' % ('; '.join(brules))
        if opts.text_color:
            prefix += '\n\nbody, p, div { color: %s !important }' % opts.text_color
        raw = prefix + opts.user_css
        raw = '::selection {background:#ffff00; color:#000;}\n' + raw
        data = 'data:text/css;charset=utf-8;base64,'
        data += b64encode(raw.encode('utf-8'))
        self.settings().setUserStyleSheetUrl(QUrl(data))

    def findText(self, q, flags):
        if self.hyphenatable:
            q = unicode(q)
            hyphenated_q = self.javascript(
                'hyphenate_text(%s, "%s")' % (json.dumps(q, ensure_ascii=False), self.loaded_lang),
                typ='string')
            if hyphenated_q and QWebPage.findText(self, hyphenated_q, flags):
                return True
        return QWebPage.findText(self, q, flags)

    def misc_config(self, opts):
        self.hyphenate = opts.hyphenate
        self.hyphenate_default_lang = opts.hyphenate_default_lang
        self.do_fit_images = opts.fit_images
        self.page_flip_duration = opts.page_flip_duration
        self.enable_page_flip = self.page_flip_duration > 0.1
        self.font_magnification_step = opts.font_magnification_step
        self.wheel_flips_pages = opts.wheel_flips_pages
        self.wheel_scroll_fraction = opts.wheel_scroll_fraction
        self.line_scroll_fraction = opts.line_scroll_fraction
        self.tap_flips_pages = opts.tap_flips_pages
        self.line_scrolling_stops_on_pagebreaks = opts.line_scrolling_stops_on_pagebreaks
        screen_width = QApplication.desktop().screenGeometry().width()
        # Leave some space for the scrollbar and some border
        self.max_fs_width = min(opts.max_fs_width, screen_width - 50)
        self.max_fs_height = opts.max_fs_height
        self.fullscreen_clock = opts.fullscreen_clock
        self.fullscreen_scrollbar = opts.fullscreen_scrollbar
        self.fullscreen_pos = opts.fullscreen_pos
        self.start_in_fullscreen = opts.start_in_fullscreen
        self.show_fullscreen_help = opts.show_fullscreen_help
        self.use_book_margins = opts.use_book_margins
        self.cols_per_screen_portrait = opts.cols_per_screen_portrait
        self.cols_per_screen_landscape = opts.cols_per_screen_landscape
        self.side_margin = opts.side_margin
        self.top_margin, self.bottom_margin = opts.top_margin, opts.bottom_margin
        self.show_controls = opts.show_controls
        self.remember_current_page = opts.remember_current_page
        self.copy_bookmarks_to_file = opts.copy_bookmarks_to_file
        self.search_online_url = opts.search_online_url or 'https://www.google.com/search?q={text}'

    def fit_images(self):
        if self.do_fit_images and not self.in_paged_mode:
            self.javascript('setup_image_scaling_handlers()')

    def add_window_objects(self):
        self.mainFrame().addToJavaScriptWindowObject("py_bridge", self)
        self.javascript('''
        Object.defineProperty(py_bridge, 'value', {
               get : function() { return JSON.parse(this._pass_json_value); },
               set : function(val) { this._pass_json_value = JSON.stringify(val); }
        });
        ''')
        self.loaded_javascript = False

    def load_javascript_libraries(self):
        if self.loaded_javascript:
            return
        self.loaded_javascript = True
        evaljs = self.mainFrame().evaluateJavaScript
        self.loaded_lang = self.js_loader(evaljs, self.current_language,
                                          self.hyphenate_default_lang)
        evaljs('window.calibre_utils.setup_epub_reading_system(%s, %s, %s, %s)' % tuple(
            map(json.dumps, (
                'calibre-desktop', __version__, 'paginated' if self.in_paged_mode else 'scrolling',
                'dom-manipulation layout-changes mouse-events keyboard-events'.split()))))
        self.javascript(
            u'window.mathjax.base = %s' % (json.dumps(self.nam.mathjax_base, ensure_ascii=False)))
        for pl in self.all_viewer_plugins:
            pl.load_javascript(evaljs)
        evaljs('py_bridge.mark_element.connect(window.calibre_extract.mark)')

    @pyqtSlot()
    def animated_scroll_done(self):
        self.animated_scroll_done_signal.emit()

    @property
    def hyphenatable(self):
        # Qt fails to render soft hyphens correctly on windows xp
        return not isxp and self.hyphenate and getattr(self, 'loaded_lang',
                                                       '') and not self.math_present

    @pyqtSlot()
    def init_hyphenate(self):
        if self.hyphenatable:
            self.javascript('do_hyphenation("%s")' % self.loaded_lang)

    @pyqtSlot(int)
    def page_turn_requested(self, backwards):
        self.page_turn.emit(bool(backwards))

    def _pass_json_value_getter(self):
        val = json.dumps(self.bridge_value)
        return val

    def _pass_json_value_setter(self, value):
        self.bridge_value = json.loads(unicode(value))

    _pass_json_value = pyqtProperty(str, fget=_pass_json_value_getter,
                                    fset=_pass_json_value_setter)

    def after_load(self, last_loaded_path=None):
        self.javascript('window.paged_display.read_document_margins()')
        self.set_bottom_padding(0)
        self.fit_images()
        w = 1 if iswindows else 0
        self.math_present = self.javascript('window.mathjax.check_for_math(%d)' % w, bool)
        self.init_hyphenate()
        self.javascript('full_screen.save_margins()')
        if self.in_fullscreen_mode:
            self.switch_to_fullscreen_mode()
        if self.in_paged_mode:
            self.switch_to_paged_mode(last_loaded_path=last_loaded_path)
        self.read_anchor_positions(use_cache=False)
        evaljs = self.mainFrame().evaluateJavaScript
        for pl in self.all_viewer_plugins:
            pl.run_javascript(evaljs)
        self.first_load = False

    def colors(self):
        self.javascript('''
            bs = getComputedStyle(document.body);
            py_bridge.value = [bs.backgroundColor, bs.color]
            ''')
        ans = self.bridge_value
        return (ans if isinstance(ans, list) else ['white', 'black'])

    def read_anchor_positions(self, use_cache=True):
        self.bridge_value = tuple(self.index_anchors)
        self.javascript(u'''
            py_bridge.value = book_indexing.anchor_positions(py_bridge.value, %s);
            ''' % ('true' if use_cache else 'false'))
        self.anchor_positions = self.bridge_value
        if not isinstance(self.anchor_positions, dict):
            # Some weird javascript error happened
            self.anchor_positions = {}
        return {k: tuple(v) for k, v in self.anchor_positions.iteritems()}

    def switch_to_paged_mode(self, onresize=False, last_loaded_path=None):
        if onresize and not self.loaded_javascript:
            return
        cols_per_screen = self.cols_per_screen_portrait if self.is_portrait else self.cols_per_screen_landscape
        cols_per_screen = max(1, min(5, cols_per_screen))
        self.javascript('''
            window.paged_display.use_document_margins = %s;
            window.paged_display.set_geometry(%d, %d, %d, %d);
            ''' % (
            ('true' if self.use_book_margins else 'false'),
            cols_per_screen, self.top_margin, self.side_margin,
            self.bottom_margin
        ))
        force_fullscreen_layout = self.nam.is_single_page(last_loaded_path)
        self.update_contents_size_for_paged_mode(force_fullscreen_layout)

    def update_contents_size_for_paged_mode(self, force_fullscreen_layout=None):
        # Setup the contents size to ensure that there is a right most margin.
        # Without this WebKit renders the final column with no margin, as the
        # columns extend beyond the boundaries (and margin) of body
        if force_fullscreen_layout is None:
            force_fullscreen_layout = self.javascript('window.paged_display.is_full_screen_layout',
                                                      typ=bool)
        f = 'true' if force_fullscreen_layout else 'false'
        side_margin = self.javascript('window.paged_display.layout(%s)' % f, typ=int)
        mf = self.mainFrame()
        sz = mf.contentsSize()
        scroll_width = self.javascript('document.body.scrollWidth', int)
        # At this point sz.width() is not reliable, presumably because Qt
        # has not yet been updated
        if scroll_width > self.window_width:
            sz.setWidth(scroll_width + side_margin)
            self.setPreferredContentsSize(sz)
        self.javascript('window.paged_display.fit_images()')

    @property
    def column_boundaries(self):
        if not self.loaded_javascript:
            return (0, 1)
        self.javascript(u'py_bridge.value = paged_display.column_boundaries()')
        return tuple(self.bridge_value)

    def after_resize(self):
        if self.in_paged_mode:
            self.setPreferredContentsSize(QSize())
            self.switch_to_paged_mode(onresize=True)
        self.javascript('if (window.mathjax) window.mathjax.after_resize();')

    def switch_to_fullscreen_mode(self):
        self.in_fullscreen_mode = True
        self.javascript('full_screen.on(%d, %d, %s)' % (self.max_fs_width, self.max_fs_height,
                                                        'true' if self.in_paged_mode else 'false'))

    def switch_to_window_mode(self):
        self.in_fullscreen_mode = False
        self.javascript('full_screen.off(%s)' % ('true' if self.in_paged_mode
                                                 else 'false'))

    @pyqtSlot(str)
    def debug(self, msg):
        prints(unicode(msg))

    @pyqtSlot(int)
    def jump_to_cfi_finished(self, job_id):
        for l in self.jump_to_cfi_listeners:
            l(job_id)

    def reference_mode(self, enable):
        self.javascript(('enter' if enable else 'leave') + '_reference_mode()')

    def set_reference_prefix(self, prefix):
        self.javascript('reference_prefix = "%s"' % prefix)

    def goto(self, ref):
        self.javascript('goto_reference("%s")' % ref)

    def goto_bookmark(self, bm):
        if bm['type'] == 'legacy':
            bm = bm['pos']
            bm = bm.strip()
            if bm.startswith('>'):
                bm = bm[1:].strip()
            self.javascript('scroll_to_bookmark("%s")' % bm)
        elif bm['type'] == 'cfi':
            self.page_position.to_pos(bm['pos'])

    def javascript(self, string, typ=None):
        ans = self.mainFrame().evaluateJavaScript(string)
        if typ in {'int', int}:
            try:
                return int(ans)
            except (TypeError, ValueError):
                return 0
        if typ in {'float', float}:
            try:
                return float(ans)
            except (TypeError, ValueError):
                return 0.0
        if typ == 'string':
            return ans or u''
        if typ in {bool, 'bool'}:
            return bool(ans)
        return ans

    def javaScriptConsoleMessage(self, msg, lineno, msgid):
        if DEBUG or self.debug_javascript:
            prints(msg)

    def javaScriptAlert(self, frame, msg):
        if DEBUG:
            prints(msg)
        else:
            return QWebPage.javaScriptAlert(self, frame, msg)

    def scroll_by(self, dx=0, dy=0):
        self.mainFrame().scroll(dx, dy)

    def scroll_to(self, x=0, y=0):
        self.mainFrame().setScrollPosition(QPoint(x, y))

    def jump_to_anchor(self, anchor):
        if not self.loaded_javascript:
            return
        self.javascript('window.paged_display.jump_to_anchor("%s")' % anchor)

    def element_ypos(self, elem):
        try:
            ans = int(elem.evaluateJavaScript('$(this).offset().top'))
        except (TypeError, ValueError):
            raise ValueError('No ypos found')
        return ans

    def elem_outer_xml(self, elem):
        return unicode(elem.toOuterXml())

    def bookmark(self):
        pos = self.page_position.current_pos
        return {'type': 'cfi', 'pos': pos}

    @property
    def at_bottom(self):
        return self.height - self.ypos <= self.window_height

    @property
    def at_top(self):
        return self.ypos <= 0

    def test(self):
        pass

    @property
    def ypos(self):
        return self.mainFrame().scrollPosition().y()

    @property
    def window_height(self):
        return self.javascript('window.innerHeight', 'int')

    @property
    def window_width(self):
        return self.javascript('window.innerWidth', 'int')

    @property
    def is_portrait(self):
        return self.window_width < self.window_height

    @property
    def xpos(self):
        return self.mainFrame().scrollPosition().x()

    @dynamic_property
    def scroll_fraction(self):
        def fget(self):
            if self.in_paged_mode:
                return self.javascript('''
                ans = 0.0;
                if (window.paged_display) {
                    ans = window.paged_display.current_pos();
                }
                ans;''', typ='float')
            else:
                try:
                    return abs(float(self.ypos) / (self.height - self.window_height))
                except ZeroDivisionError:
                    return 0.

        def fset(self, val):
            if self.in_paged_mode and self.loaded_javascript:
                self.javascript('paged_display.scroll_to_pos(%f)' % val)
            else:
                npos = val * (self.height - self.window_height)
                if npos < 0:
                    npos = 0
                self.scroll_to(x=self.xpos, y=npos)

        return property(fget=fget, fset=fset)

    @dynamic_property
    def page_number(self):
        ' The page number is the number of the page at the left most edge of the screen (starting from 0) '

        def fget(self):
            if self.in_paged_mode:
                return self.javascript(
                    'ans = 0; if (window.paged_display) ans = window.paged_display.column_boundaries()[0]; ans;',
                    typ='int')

        def fset(self, val):
            if self.in_paged_mode and self.loaded_javascript:
                self.javascript(
                    'if (window.paged_display) window.paged_display.scroll_to_column(%d)' % int(
                        val))
                return True

        return property(fget=fget, fset=fset)

    @property
    def page_dimensions(self):
        if self.in_paged_mode:
            return self.javascript(
                '''
                ans = ''
                if (window.paged_display)
                    ans = window.paged_display.col_width + ':' + window.paged_display.current_page_height;
                ans;''', typ='string')

    @property
    def hscroll_fraction(self):
        try:
            return float(self.xpos) / self.width
        except ZeroDivisionError:
            return 0.

    @property
    def height(self):
        # Note that document.body.offsetHeight does not include top and bottom
        # margins on body and in some cases does not include the top margin on
        # the first element inside body either. See ticket #8791 for an example
        # of the latter.
        q = self.mainFrame().contentsSize().height()
        if q < 0:
            # Don't know if this is still needed, but it can't hurt
            j = self.javascript('document.body.offsetHeight', 'int')
            if j >= 0:
                q = j
        return q

    @property
    def width(self):
        return self.mainFrame().contentsSize().width()  # offsetWidth gives inaccurate results

    def set_bottom_padding(self, amount):
        s = QSize(-1, -1) if amount == 0 else QSize(self.viewportSize().width(),
                                                    self.height + amount)
        self.setPreferredContentsSize(s)

    def extract_node(self):
        return unicode(self.mainFrame().evaluateJavaScript(
            'window.calibre_extract.extract()'))


def apply_settings(settings, opts):
    settings.setFontSize(QWebSettings.DefaultFontSize, opts.default_font_size)
    settings.setFontSize(QWebSettings.DefaultFixedFontSize, opts.mono_font_size)
    settings.setFontSize(QWebSettings.MinimumLogicalFontSize, opts.minimum_font_size)
    settings.setFontSize(QWebSettings.MinimumFontSize, opts.minimum_font_size)
    settings.setFontFamily(QWebSettings.StandardFont,
                           {'serif': opts.serif_family, 'sans': opts.sans_family,
                            'mono': opts.mono_family}[
                               opts.standard_font])
    settings.setFontFamily(QWebSettings.SerifFont, opts.serif_family)
    settings.setFontFamily(QWebSettings.SansSerifFont, opts.sans_family)
    settings.setFontFamily(QWebSettings.FixedFont, opts.mono_family)
    settings.setAttribute(QWebSettings.ZoomTextOnly, True)


def secure_web_page(qwebpage_or_qwebsettings):
    from PyQt5.QtWebKit import QWebSettings
    settings = qwebpage_or_qwebsettings if isinstance(qwebpage_or_qwebsettings,
                                                      QWebSettings) else qwebpage_or_qwebsettings.settings()
    settings.setAttribute(QWebSettings.JavaEnabled, False)
    settings.setAttribute(QWebSettings.PluginsEnabled, False)
    settings.setAttribute(QWebSettings.JavascriptCanOpenWindows, False)
    settings.setAttribute(QWebSettings.JavascriptCanAccessClipboard, False)
    settings.setAttribute(QWebSettings.LocalContentCanAccessFileUrls,
                          False)  # ensure javascript cannot read from local files
    settings.setAttribute(QWebSettings.NotificationsEnabled, False)
    settings.setThirdPartyCookiePolicy(QWebSettings.AlwaysBlockThirdPartyCookies)
    return settings


def apply_basic_settings(settings):
    secure_web_page(settings)
    # PrivateBrowsing disables console messages
    # settings.setAttribute(QWebSettings.PrivateBrowsingEnabled, True)

    # Miscellaneous
    settings.setAttribute(QWebSettings.LinksIncludedInFocusChain, True)


class PagePosition(object):

    def __init__(self, document):
        self.document = document
        document.jump_to_cfi_listeners.add(self)
        self.cfi_job_id = 0
        self.pending_scrolls = set()

    @property
    def viewport_cfi(self):
        ans = self.document.mainFrame().evaluateJavaScript('''
            ans = 'undefined';
            if (window.paged_display) {
                ans = window.paged_display.current_cfi();
                if (!ans) ans = 'undefined';
            }
            ans;
        ''')
        if ans in {'', 'undefined'}:
            ans = None
        return ans

    def scroll_to_cfi(self, cfi):
        if cfi:
            jid = self.cfi_job_id
            self.cfi_job_id += 1
            cfi = json.dumps(cfi)
            self.pending_scrolls.add(jid)
            self.document.mainFrame().evaluateJavaScript(
                    'paged_display.jump_to_cfi(%s, %d)' % (cfi, jid))
            # jump_to_cfi is async, so we wait for it to complete
            st = time.time()
            WAIT = 1  # seconds
            while jid in self.pending_scrolls and time.time() - st < WAIT:
                QApplication.processEvents(QEventLoop.ExcludeUserInputEvents | QEventLoop.ExcludeSocketNotifiers)
                time.sleep(0.01)
            if jid in self.pending_scrolls:
                self.pending_scrolls.discard(jid)
                if DEBUG:
                    print ('jump_to_cfi() failed to complete after %s seconds' % WAIT)

    @property
    def current_pos(self):
        ans = self.viewport_cfi
        if not ans:
            ans = self.document.scroll_fraction
        return ans

    def __enter__(self):
        self.save()

    def __exit__(self, *args):
        self.restore()

    def __call__(self, cfi_job_id):
        self.pending_scrolls.discard(cfi_job_id)

    def save(self, overwrite=True):
        if not overwrite and self._cpos is not None:
            return
        self._cpos = self.current_pos

    def restore(self):
        if self._cpos is None:
            return
        self.to_pos(self._cpos)
        self._cpos = None

    def to_pos(self, pos):
        if isinstance(pos, (int, float)):
            self.document.scroll_fraction = pos
        else:
            self.scroll_to_cfi(pos)

    def set_pos(self, pos):
        self._cpos = pos


class JavaScriptLoader(object):
    with open(filepath_relative(sys.modules[__name__], "json")) as iput:
        options = json.load(iput)

    JS = {x: ('viewer/%s.js' % x if y is None else y) for x, y in options["js"].iteritems()}
    CS = options["cs"]
    ORDER = options["order"]

    def __init__(self, dynamic_coffeescript=False):
        self._dynamic_coffeescript = dynamic_coffeescript
        if self._dynamic_coffeescript:
            try:
                from calibre.utils.serve_coffee import compile_coffeescript;
                compile_coffeescript
            except:
                self._dynamic_coffeescript = False
                print('WARNING: Failed to load serve_coffee, not compiling coffeescript ' \
                      'dynamically.')

        self._cache = {}
        self._hp_cache = {}

    def get(self, name):
        ans = self._cache.get(name, None)
        if ans is None:
            src = self.CS.get(name, None)
            if src is None:
                src = self.JS.get(name, None)
                if src is None:
                    raise KeyError('No such resource: %s' % name)
                ans = P(src, data=True,
                        allow_user_override=False).decode('utf-8')
            else:
                dynamic = (self._dynamic_coffeescript and
                           calibre.__file__ and not calibre.__file__.endswith('.pyo') and
                           os.path.exists(calibre.__file__))
                ans = compiled_coffeescript(src, dynamic=dynamic).decode('utf-8')
            self._cache[name] = ans

        return ans

    def __call__(self, evaljs, lang, default_lang):
        for x in self.ORDER:
            src = self.get(x)
            evaljs(src)

        if not lang:
            lang = default_lang or 'en'

        def lang_name(l):
            l = l.lower()
            l = lang_as_iso639_1(l)
            if not l:
                l = 'en'
            l = {'en': 'en-us', 'nb': 'nb-no', 'el': 'el-monoton'}.get(l, l)
            return l.lower().replace('_', '-')

        if not self._hp_cache:
            with zipfile.ZipFile(
                    P('viewer/hyphenate/patterns.zip', allow_user_override=False), 'r') as zf:
                for pat in zf.namelist():
                    raw = zf.read(pat).decode('utf-8')
                    self._hp_cache[pat.partition('.')[0]] = raw

        if lang_name(lang) not in self._hp_cache:
            lang = lang_name(default_lang)

        lang = lang_name(lang)

        evaljs('\n\n'.join(self._hp_cache.itervalues()))

        return lang