#!/usr/bin/env  python2

import json
import math
import sys
from functools import partial
from future_builtins import map

from PyQt5.Qt import (QSize, QUrl, Qt, QPainter, QBrush, QImage, QRegion, QIcon, QAction, QMenu,
                      pyqtSignal, QApplication, QKeySequence, QMimeData)
from PyQt5.QtWebKitWidgets import QWebView

from calibre.constants import iswindows
from calibre.ebooks.oeb.display.webview import load_html
from calibre.gui2 import open_url, error_dialog
from calibre.gui2.shortcuts import Shortcuts
from calibre.gui2.viewer.qdialog.gestures import GestureHandler
from calibre.gui2.viewer.qdialog.qdialogConfig import config, load_themes
from calibre.gui2.viewer.qdialog.qdialogImage import ImagePopup
from calibre.gui2.viewer.qdialog.qdialogInspect import QdialogInspect
from calibre.gui2.viewer.qdialog.qdialogTablePopup import TablePopup
from calibre.gui2.viewer.qwebpage.qwebpageDocument import Document
from calibre.gui2.viewer.qwebpage.qwebpageFootnote import Footnotes
from calibre.gui2.viewer.qwidget.qwidgetSlideFlip import QwidgetSlideFlip
from calibre.library.filepath import filepath_relative

__license__ = 'GPL v3'
__copyright__ = '2008, Kovid Goyal kovid@kovidgoyal.net'
__docformat__ = 'restructuredtext en'

_ = _
I = I
dynamic_property = dynamic_property

with open(filepath_relative(sys.modules[__name__], "json")) as iput:
    SHORTCUTS = {
        name: (shortcuts, _(tooltip))
        for name, (shortcuts, tooltip) in json.load(iput)["shortcuts"].items()
        }


class QwebviewDocument(QWebView):
    magnification_changed = pyqtSignal(object)
    DISABLED_BRUSH = QBrush(Qt.lightGray, Qt.Dense5Pattern)
    gesture_handler = lambda s, e: False
    last_loaded_path = None
    context_actions = []

    def set_footnotes_view(self, view):
        self.footnotes.set_footnotes_view(view)
        view.follow_link.connect(self.follow_footnote_link)

    def initialize_view(self, debug_javascript=False):
        self._ignore_scrollbar_signals = False
        self._reference_mode = False
        self._size_hint = QSize(510, 680)
        self.debug_javascript = debug_javascript
        self.flipper = QwidgetSlideFlip(self)
        self.footnotes = Footnotes(self)
        self.gesture_handler = GestureHandler(self)
        self.goto_location_actions = {}
        self.goto_location_menu = QMenu(self)
        self.image_popup = ImagePopup(self)
        self.initial_pos = 0.0
        self.is_auto_repeat_event = False
        self.loading_url = None
        self.manager = None
        self.search_online_menu = QMenu(self)
        self.shortcuts = Shortcuts(SHORTCUTS, 'shortcuts/viewer')
        self.table_popup = TablePopup(self)
        self.to_bottom = False
        self.qmenuSynopsis = QMenu(self)

        self.document = d = Document(
            self.shortcuts, parent=self, debug_javascript=debug_javascript)
        d.nam.load_error.connect(self.on_unhandled_load_error)
        d.settings_changed.connect(self.footnotes.clone_settings)
        d.animated_scroll_done_signal.connect(self.animated_scroll_done, type=Qt.QueuedConnection)
        d.linkClicked.connect(self.link_clicked)
        d.linkHovered.connect(self.link_hovered)
        d.page_turn.connect(self.page_turn_requested)
        d.selectionChanged[()].connect(self.selection_changed)

        self.inspector = QdialogInspect(self, d)

        self.loadFinished.connect(self.load_finished)
        self.setPage(d)

        a = [
            d.DownloadImageToDisk, d.OpenLinkInNewWindow, d.DownloadLinkToDisk,
            d.OpenImageInNewWindow, d.OpenLink, d.Reload, d.InspectElement]
        self.unimplemented_actions = list(map(self.pageAction, a))

        with open(filepath_relative(self, "json")) as iput:
            actions = json.load(iput)

        self.create_actions(actions["root"])
        self.create_online_actions(actions["search_online"])
        self.create_synopsis_actions(actions["synopsis"])
        self.create_goto_actions(actions["goto_location"])

        self.synopsis_action.setMenu(self.qmenuSynopsis)
        self.search_online_action.setMenu(self.search_online_menu)
        self.goto_location_action.setMenu(self.goto_location_menu)

        self.copy_action.setIcon(QIcon(I('edit-copy.png')))
        self.copy_action.triggered.connect(self.copy, Qt.QueuedConnection)

    # --- actions
    def create_synopsis_action(self, name, text, section=None, slot=None, icon=None, shortcut=None,
                               separator=False, actions=None, qmenu=None):
        qmenu = qmenu if qmenu else self.qmenuSynopsis
        qaction = qmenu.addAction(_(text))
        shortcuts = self.shortcuts.get_sequences(shortcut)
        if shortcuts:
            qaction.setShortcut(shortcuts[0])
        if section:
            qaction.setData(section)
        if slot:
            qaction.triggered.connect(getattr(self, slot))
        if icon:
            qaction.setIcon(QIcon(I(icon)))
        if separator:
            qmenu.addSeparator()
        if actions:
            q = QMenu(self)
            qaction.setMenu(q)
            self.create_synopsis_actions(actions, q)

        setattr(self, name + "_action", qaction)
        self.addAction(qaction)

    def create_synopsis_actions(self, actions, qmenu=None):
        for options in actions:
            self.create_synopsis_action(qmenu=qmenu, **options)

    def create_goto_action(self, name, call, shortcut, separator=False):
        call = getattr(self, call)

        self.goto_location_actions[shortcut] = call
        self.goto_location_menu.addAction(_(name), call, self.shortcuts.get_sequences(shortcut)[0])

        if separator:
            self.goto_location_menu.addSeparator()

    def create_goto_actions(self, actions):
        for options in actions:
            self.create_goto_action(**options)

    def create_online_action(self, name, url=None, icon=None, separator=False, shortcut=None,
                             actions=None, qmenu=None):
        qmenu = qmenu if qmenu else self.search_online_menu
        qaction = qmenu.addAction(name, self.search_online)

        if url:
            qaction.setData(url)
        shortcuts = self.shortcuts.get_sequences(shortcut)
        if shortcuts:
            qaction.setShortcut(shortcuts[0])
        if icon:
            qaction.setIcon(QIcon(I(icon)))
        if separator:
            qmenu.addSeparator()
        if actions:
            q = QMenu(self)
            qaction.setMenu(q)
            self.create_online_actions(actions, q)

    def create_online_actions(self, actions, qmenu=None):
        for action_options in actions:
            self.create_online_action(qmenu=qmenu, **action_options)

    def create_action(self, name, text, slot=None, icon=None, checkable=False, shortcut=None,
                      context=False, separator=False):
        action = QAction(_(text), self)
        action.setCheckable(checkable)
        action.setData(shortcut)

        if slot:
            action.triggered.connect(getattr(self, slot))
        if icon:
            action.setIcon(QIcon(I(icon)))
        if context:
            self.context_actions.append(action)
        if separator:
            action_separator = QAction(self)
            action_separator.setSeparator(True)

            self.context_actions.append(action_separator)

        setattr(self, name + "_action", action)
        self.addAction(action)

    def copy_markdown(self, *args, **kwargs):
        self.copy_text(self.selected_markdown_body())

    def synopsis_append(self, *args, **kwargs):
        section = self.sender().data().lower()
        if section == "body":
            text = self.selected_markdown_body()
        elif section == "header":
            text = self.selected_markdown_header(int(self.sender().text()))
        else:
            raise NotImplementedError(section)

        if text:
            self.manager.qdockwidgetSynopsis.append(text)

    def selected_markdown_header(self, level):
        if self.selected_text:
            return "\n{0} <a class='header' position='{1}'>{2}</a>".format(
                "#" * level, self.document.page_position.current_pos, self.selected_text)

    def selected_markdown_body(self):
        if self.selected_text:
            return "\n{0}\n{{: position={1}}}".format(
                self.selected_text, self.document.page_position.current_pos)

    def create_actions(self, actions):
        for action_options in actions:
            self.create_action(**action_options)

    # --- goto
    def goto_next_section(self, *args):
        if self.manager is not None:
            self.manager.goto_next_section()

    def goto_previous_section(self, *args):
        if self.manager is not None:
            self.manager.goto_previous_section()

    def goto_document_start(self, *args):
        if self.manager is not None:
            self.manager.goto_start()

    def goto_document_end(self, *args):
        if self.manager is not None:
            self.manager.goto_end()

    def goto_section_start(self):
        self.scroll_to(0)

    def goto_section_end(self):
        self.scroll_to(1)

    def goto(self, ref):
        self.document.goto(ref)

    def goto_bookmark(self, bm):
        self.document.goto_bookmark(bm)

    # ----
    @property
    def copy_action(self):
        return self.pageAction(self.document.Copy)

    def animated_scroll_done(self):
        if self.manager is not None:
            self.manager.scrolled(self.document.scroll_fraction)

    def reference_mode(self, enable):
        self._reference_mode = enable
        self.document.reference_mode(enable)

    def config(self, parent=None):
        self.document.do_config(parent)
        if self.document.in_fullscreen_mode:
            self.document.switch_to_fullscreen_mode()
        self.setFocus(Qt.OtherFocusReason)

    def load_theme(self, theme_id):
        themes = load_themes()
        theme = themes[theme_id]
        opts = config(theme).parse()
        self.document.apply_settings(opts)
        if self.document.in_fullscreen_mode:
            self.document.switch_to_fullscreen_mode()
        self.setFocus(Qt.OtherFocusReason)

    def bookmark(self):
        return self.document.bookmark()

    @property
    def selected_text(self):
        return self.document.selectedText().replace(u'\u00ad', u'').strip()

    def copy_position(self):
        self.copy_text(self.document.page_position.current_pos)

    def copy_text(self, text):
        QApplication.clipboard().setText(text)

    def copy(self):
        self.document.triggerAction(self.document.Copy)
        c = QApplication.clipboard()
        md = c.mimeData()
        if iswindows:
            nmd = QMimeData()
            nmd.setHtml(md.html().replace(u'\u00ad', ''))
            md = nmd
        md.setText(self.selected_text)
        QApplication.clipboard().setMimeData(md)

    def selection_changed(self):
        if self.manager is not None:
            self.manager.selection_changed(self.selected_text)

    def _selectedText(self):
        t = unicode(self.selectedText()).strip()
        if not t:
            return u''
        if len(t) > 40:
            t = t[:40] + u'...'
        t = t.replace(u'&', u'&&')
        return _("S&earch online for '%s'") % t

    def popup_table(self):
        html = self.document.extract_node()
        self.table_popup(html, self.as_url(self.last_loaded_path),
                         self.document.font_magnification_step)

    def contextMenuEvent(self, ev):
        from_touch = ev.reason() == ev.Other
        mf = self.document.mainFrame()
        r = mf.hitTestContent(ev.pos())
        img = r.pixmap()
        elem = r.element()
        if elem.isNull():
            elem = r.enclosingBlockElement()
        table = None
        parent = elem
        while not parent.isNull():
            if (unicode(parent.tagName()) == u'table' or unicode(parent.localName()) == u'table'):
                table = parent
                break
            parent = parent.parent()

        self.image_popup.current_img = img
        self.image_popup.current_url = r.imageUrl()
        menu = self.document.createStandardContextMenu()
        for action in self.unimplemented_actions:
            menu.removeAction(action)

        for action in menu.actions():
            if action.isSeparator():
                menu.removeAction(action)

        if not img.isNull():
            menu.addAction(self.view_image_action)
        if table is not None:
            self.document.mark_element.emit(table)
            menu.addAction(self.view_table_action)

        text = self._selectedText()
        if text and img.isNull():
            self.search_online_action.setText(text)
            for action in self.context_actions:
                if action.isSeparator():
                    menu.addSeparator()
                    continue

                text = unicode(action.text())
                shortcuts = self.shortcuts.get_shortcuts(action.data())
                if shortcuts:
                    text += ' [{0}]'.format(','.join(shortcuts))

                menu_action = menu.addAction(action.icon(), text, action.trigger)
                menu_action.setMenu(action.menu())

        if from_touch and self.manager is not None:
            word = unicode(mf.evaluateJavaScript(
                'window.calibre_utils.word_at_point(%f, %f)' % (ev.pos().x(), ev.pos().y())) or '')
            if word:
                menu.addAction(
                    self.dictionary_action.icon(),
                    _('Lookup %s in the dictionary') % word,
                    partial(self.manager.lookup, word))
                menu.addAction(
                    self.search_online_action.icon(),
                    _('Search for %s online') % word,
                    partial(self.do_search_online, word))

        if not text and img.isNull():
            menu.addSeparator()
            if self.manager.action_back.isEnabled():
                menu.addAction(self.manager.action_back)
            if self.manager.action_forward.isEnabled():
                menu.addAction(self.manager.action_forward)

            menu.addAction(self.copy_position_action)
            menu.addAction(self.goto_location_action)
            if self.manager is not None:
                menu.addActions(self.manager.context_actions)
                menu.addAction(self.manager.action_reload)
                menu.addAction(self.manager.action_quit)
                menu.insertAction(self.manager.action_font_size_larger, self.restore_fonts_action)

                self.restore_fonts_action.setChecked(self.multiplier == 1)

        menu.addSeparator()
        menu.addAction(_('Inspect'), self.inspect)

        for plugin in self.document.all_viewer_plugins:
            plugin.customize_context_menu(menu, ev, r)

        if from_touch:
            from calibre.constants import plugins
            pi = plugins['progress_indicator'][0]
            for name in (menu, self.goto_location_menu):
                if hasattr(pi, 'set_touch_menu_style'):
                    pi.set_touch_menu_style(name)
            helpt = QAction(QIcon(I('help.png')), _('Show supported touch screen gestures'), menu)
            helpt.triggered.connect(self.gesture_handler.show_help)
            menu.insertAction(menu.actions()[0], helpt)
        else:
            self.goto_location_menu.setStyle(self.style())

        self.context_menu = menu
        menu.exec_(ev.globalPos())

    def inspect(self):
        self.inspector.show()
        self.inspector.raise_()
        self.pageAction(self.document.InspectElement).trigger()

    def lookup(self, *args):
        if self.manager is not None:
            t = unicode(self.selectedText()).strip()
            if t:
                self.manager.lookup(t.split()[0])

    def search_next(self):
        if self.manager is not None:
            t = unicode(self.selectedText()).strip()
            if t:
                self.manager.search.set_search_string(t)

    def search_online(self):
        t = unicode(self.selectedText()).strip()
        if t:
            self.do_search_online(t, self.sender())

    def do_search_online(self, text, action):
        # url = self.document.search_online_url.replace('%s', QUrl().toPercentEncoding(text))
        url = action.data().replace('%s', QUrl().toPercentEncoding(text))
        if not isinstance(url, bytes):
            url = url.encode('utf-8')

        open_url(QUrl.fromEncoded(url))

    def set_manager(self, manager):
        self.manager = manager
        self.scrollbar = manager.horizontal_scrollbar
        self.scrollbar.valueChanged[(int)].connect(self.scroll_horizontally)

    def scroll_horizontally(self, amount):
        self.document.scroll_to(y=self.document.ypos, x=amount)

    @property
    def scroll_pos(self):
        return (self.document.ypos, self.document.ypos +
                self.document.window_height)

    @property
    def viewport_rect(self):
        # (left, top, right, bottom) of the viewport in document co-ordinates
        # When in paged mode, left and right are the numbers of the columns
        # at the left edge and *after* the right edge of the viewport
        d = self.document
        if d.in_paged_mode:
            try:
                l, r = d.column_boundaries
            except ValueError:
                l, r = (0, 1)
        else:
            l, r = d.xpos, d.xpos + d.window_width
        return (l, d.ypos, r, d.ypos + d.window_height)

    def link_hovered(self, link, text, context):
        link, text = unicode(link), unicode(text)
        if link:
            self.setCursor(Qt.PointingHandCursor)
        else:
            self.unsetCursor()

    def link_clicked(self, url):
        if self.manager is not None:
            self.manager.link_clicked(url)

    def sizeHint(self):
        return self._size_hint

    @dynamic_property
    def scroll_fraction(self):
        def fget(self):
            return self.document.scroll_fraction

        def fset(self, val):
            self.document.scroll_fraction = float(val)

        return property(fget=fget, fset=fset)

    @property
    def hscroll_fraction(self):
        return self.document.hscroll_fraction

    @property
    def content_size(self):
        return self.document.width, self.document.height

    @dynamic_property
    def current_language(self):
        def fget(self):
            return self.document.current_language

        def fset(self, val):
            self.document.current_language = val

        return property(fget=fget, fset=fset)

    def search(self, text, backwards=False):
        flags = self.document.FindBackward if backwards else self.document.FindFlags(0)
        found = self.document.findText(text, flags)
        if found and self.document.in_paged_mode:
            self.document.javascript('paged_display.snap_to_selection()')
        return found

    def path(self, url=None):
        url = url or self.url()
        return self.document.nam.as_abspath(url)

    def as_url(self, path):
        return self.document.nam.as_url(path)

    def load_path(self, path, pos=0.0):
        self.initial_pos = pos
        self.last_loaded_path = path
        # This is needed otherwise percentage margins on body are not correctly
        # evaluated in read_document_margins() in paged mode.
        self.document.setPreferredContentsSize(QSize())

        url = self.as_url(path)
        entries = set()
        for ie in getattr(path, 'index_entries', []):
            if ie.start_anchor:
                entries.add(ie.start_anchor)
            if ie.end_anchor:
                entries.add(ie.end_anchor)
        self.document.index_anchors = entries

        def callback(lu):
            self.loading_url = lu
            if self.manager is not None:
                self.manager.load_started()

        load_html(path, self, codec=getattr(path, 'encoding', 'utf-8'), mime_type=getattr(path,
                                                                                          'mime_type',
                                                                                          'text/html'),
                  loading_url=url, pre_load_callback=callback)

    def on_unhandled_load_error(self, name, tb):
        error_dialog(self, _('Failed to load file'), _(
            'Failed to load the file: {}. Click "Show details" for more information').format(name),
                     det_msg=tb,
                     show=True)

    def initialize_scrollbar(self):
        if getattr(self, 'scrollbar', None) is not None:
            if self.document.in_paged_mode:
                self.scrollbar.setVisible(False)
                return
            delta = self.document.width - self.size().width()
            if delta > 0:
                self._ignore_scrollbar_signals = True
                self.scrollbar.blockSignals(True)
                self.scrollbar.setRange(0, delta)
                self.scrollbar.setValue(0)
                self.scrollbar.setSingleStep(1)
                self.scrollbar.setPageStep(int(delta / 10.))
            self.scrollbar.setVisible(delta > 0)
            self.scrollbar.blockSignals(False)
            self._ignore_scrollbar_signals = False

    def load_finished(self, ok):
        if self.loading_url is None:
            # An <iframe> finished loading
            return
        self.loading_url = None
        self.document.load_javascript_libraries()
        self.document.after_load(self.last_loaded_path)
        self._size_hint = self.document.mainFrame().contentsSize()
        scrolled = False
        if self.to_bottom:
            self.to_bottom = False
            self.initial_pos = 1.0
        if self.initial_pos > 0.0:
            scrolled = True
        self.scroll_to(self.initial_pos, notify=False)
        self.initial_pos = 0.0
        self.update()
        self.initialize_scrollbar()
        self.document.reference_mode(self._reference_mode)
        if self.manager is not None:
            spine_index = self.manager.load_finished(bool(ok))
            if spine_index > -1:
                self.document.set_reference_prefix('%d.' % (spine_index + 1))
            if scrolled:
                self.manager.scrolled(self.document.scroll_fraction,
                                      onload=True)

        if self.flipper.isVisible():
            if self.flipper.running:
                self.flipper.setVisible(False)
            else:
                self.flipper(self.current_page_image(),
                             duration=self.document.page_flip_duration)

    @classmethod
    def test_line(cls, img, y):
        'Test if line contains pixels of exactly the same color'
        start = img.pixel(0, y)
        for i in range(1, img.width()):
            if img.pixel(i, y) != start:
                return False
        return True

    def current_page_image(self, overlap=-1):
        if overlap < 0:
            overlap = self.height()
        img = QImage(self.width(), overlap, QImage.Format_ARGB32_Premultiplied)
        painter = QPainter(img)
        painter.setRenderHints(self.renderHints())
        self.document.mainFrame().render(painter, QRegion(0, 0, self.width(), overlap))
        painter.end()
        return img

    def find_next_blank_line(self, overlap):
        img = self.current_page_image(overlap)
        for i in range(overlap - 1, -1, -1):
            if self.test_line(img, i):
                self.scroll_by(y=i, notify=False)
                return
        self.scroll_by(y=overlap)

    def previous_page(self):
        if self.flipper.running and not self.is_auto_repeat_event:
            return
        if self.loading_url is not None:
            return
        epf = self.document.enable_page_flip and not self.is_auto_repeat_event

        if self.document.in_paged_mode:
            loc = self.document.javascript(
                'paged_display.previous_screen_location()', typ='int')
            if loc < 0:
                if self.manager is not None:
                    if epf:
                        self.flipper.initialize(self.current_page_image(),
                                                forwards=False)
                    self.manager.previous_document()
            else:
                if epf:
                    self.flipper.initialize(self.current_page_image(),
                                            forwards=False)
                self.document.scroll_to(x=loc, y=0)
                if epf:
                    self.flipper(self.current_page_image(),
                                 duration=self.document.page_flip_duration)
                if self.manager is not None:
                    self.manager.scrolled(self.scroll_fraction)

            return

        delta_y = self.document.window_height - 25
        if self.document.at_top:
            if self.manager is not None:
                self.to_bottom = True
                if epf:
                    self.flipper.initialize(self.current_page_image(), False)
                self.manager.previous_document()
        else:
            opos = self.document.ypos
            upper_limit = opos - delta_y
            if upper_limit < 0:
                upper_limit = 0
            if upper_limit < opos:
                if epf:
                    self.flipper.initialize(self.current_page_image(),
                                            forwards=False)
                self.document.scroll_to(self.document.xpos, upper_limit)
                if epf:
                    self.flipper(self.current_page_image(),
                                 duration=self.document.page_flip_duration)
                if self.manager is not None:
                    self.manager.scrolled(self.scroll_fraction)

    def next_page(self):
        if self.flipper.running and not self.is_auto_repeat_event:
            return
        if self.loading_url is not None:
            return
        epf = self.document.enable_page_flip and not self.is_auto_repeat_event

        if self.document.in_paged_mode:
            loc = self.document.javascript(
                'paged_display.next_screen_location()', typ='int')
            if loc < 0:
                if self.manager is not None:
                    if epf:
                        self.flipper.initialize(self.current_page_image())
                    self.manager.next_document()
            else:
                if epf:
                    self.flipper.initialize(self.current_page_image())
                self.document.scroll_to(x=loc, y=0)
                if epf:
                    self.flipper(self.current_page_image(),
                                 duration=self.document.page_flip_duration)
                if self.manager is not None:
                    self.manager.scrolled(self.scroll_fraction)

            return

        window_height = self.document.window_height
        document_height = self.document.height
        ddelta = document_height - window_height
        # print '\nWindow height:', window_height
        # print 'Document height:', self.document.height

        delta_y = window_height - 25
        if self.document.at_bottom or ddelta <= 0:
            if self.manager is not None:
                if epf:
                    self.flipper.initialize(self.current_page_image())
                self.manager.next_document()
        elif ddelta < 25:
            self.scroll_by(y=ddelta)
            return
        else:
            oopos = self.document.ypos
            # print 'Original position:', oopos
            self.document.set_bottom_padding(0)
            opos = self.document.ypos
            # print 'After set padding=0:', self.document.ypos
            if opos < oopos:
                if self.manager is not None:
                    if epf:
                        self.flipper.initialize(self.current_page_image())
                    self.manager.next_document()
                return
            # oheight = self.document.height
            lower_limit = opos + delta_y  # Max value of top y co-ord after scrolling
            max_y = self.document.height - window_height  # The maximum possible top y co-ord
            if max_y < lower_limit:
                padding = lower_limit - max_y
                if padding == window_height:
                    if self.manager is not None:
                        if epf:
                            self.flipper.initialize(self.current_page_image())
                        self.manager.next_document()
                    return
                # print 'Setting padding to:', lower_limit - max_y
                self.document.set_bottom_padding(lower_limit - max_y)
            if epf:
                self.flipper.initialize(self.current_page_image())
            # print 'Document height:', self.document.height
            # print 'Height change:', (self.document.height - oheight)
            max_y = self.document.height - window_height
            lower_limit = min(max_y, lower_limit)
            # print 'Scroll to:', lower_limit
            if lower_limit > opos:
                self.document.scroll_to(self.document.xpos, lower_limit)
            actually_scrolled = self.document.ypos - opos
            # print 'After scroll pos:', self.document.ypos
            # print 'Scrolled by:', self.document.ypos - opos
            self.find_next_blank_line(window_height - actually_scrolled)
            # print 'After blank line pos:', self.document.ypos
            if epf:
                self.flipper(self.current_page_image(),
                             duration=self.document.page_flip_duration)
            if self.manager is not None:
                self.manager.scrolled(self.scroll_fraction)
                # print 'After all:', self.document.ypos

    def page_turn_requested(self, backwards):
        if backwards:
            self.previous_page()
        else:
            self.next_page()

    def scroll_by(self, x=0, y=0, notify=True):
        old_pos = (self.document.xpos if self.document.in_paged_mode else
                   self.document.ypos)
        self.document.scroll_by(x, y)
        new_pos = (self.document.xpos if self.document.in_paged_mode else
                   self.document.ypos)
        if notify and self.manager is not None and new_pos != old_pos:
            self.manager.scrolled(self.scroll_fraction)

    def scroll_to(self, pos, notify=True):
        if self._ignore_scrollbar_signals:
            return
        old_pos = (self.document.xpos if self.document.in_paged_mode else
                   self.document.ypos)
        if self.document.in_paged_mode:
            if isinstance(pos, basestring):
                self.document.jump_to_anchor(pos)
            else:
                self.document.scroll_fraction = pos
        else:
            if isinstance(pos, basestring):
                self.document.jump_to_anchor(pos)
            else:
                if pos >= 1:
                    self.document.scroll_to(0, self.document.height)
                else:
                    y = int(math.ceil(
                        pos * (self.document.height - self.document.window_height)))
                    self.document.scroll_to(0, y)

        new_pos = (self.document.xpos if self.document.in_paged_mode else
                   self.document.ypos)
        if notify and self.manager is not None and new_pos != old_pos:
            self.manager.scrolled(self.scroll_fraction)

    @dynamic_property
    def multiplier(self):
        def fget(self):
            return self.zoomFactor()

        def fset(self, val):
            oval = self.zoomFactor()
            self.setZoomFactor(val)
            if val != oval:
                if self.document.in_paged_mode:
                    self.document.update_contents_size_for_paged_mode()
                self.magnification_changed.emit(val)

        return property(fget=fget, fset=fset)

    def magnify_fonts(self, amount=None):
        if amount is None:
            amount = self.document.font_magnification_step
        with self.document.page_position:
            self.multiplier += amount
        return self.document.scroll_fraction

    def shrink_fonts(self, amount=None):
        if amount is None:
            amount = self.document.font_magnification_step
        if self.multiplier >= amount:
            with self.document.page_position:
                self.multiplier -= amount
        return self.document.scroll_fraction

    def restore_font_size(self):
        with self.document.page_position:
            self.multiplier = 1
        return self.document.scroll_fraction

    def changeEvent(self, event):
        if event.type() == event.EnabledChange:
            self.update()
        return QWebView.changeEvent(self, event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHints(self.renderHints())
        self.document.mainFrame().render(painter, event.region())
        if not self.isEnabled():
            painter.fillRect(event.region().boundingRect(), self.DISABLED_BRUSH)
        painter.end()

    def wheelEvent(self, event):
        if event.phase() not in (Qt.ScrollUpdate, 0):
            # 0 is Qt.NoScrollPhase which is not yet available in PyQt
            return
        mods = event.modifiers()
        num_degrees = event.angleDelta().y() // 8
        if mods & Qt.CTRL:
            if self.manager is not None and num_degrees != 0:
                (self.manager.font_size_larger if num_degrees > 0 else
                 self.manager.font_size_smaller)()
                return

        if self.document.in_paged_mode:
            if abs(num_degrees) < 15:
                return
            typ = 'screen' if self.document.wheel_flips_pages else 'col'
            direction = 'next' if num_degrees < 0 else 'previous'
            loc = self.document.javascript('paged_display.%s_%s_location()' % (
                direction, typ), typ='int')
            if loc > -1:
                self.document.scroll_to(x=loc, y=0)
                if self.manager is not None:
                    self.manager.scrolled(self.scroll_fraction)
                event.accept()
            elif self.manager is not None:
                if direction == 'next':
                    self.manager.next_document()
                else:
                    self.manager.previous_document()
                event.accept()
            return

        if num_degrees < -14:
            if self.document.wheel_flips_pages:
                self.next_page()
                event.accept()
                return
            if self.document.at_bottom:
                self.scroll_by(y=15)  # at_bottom can lie on windows
                if self.manager is not None:
                    self.manager.next_document()
                    event.accept()
                    return
        elif num_degrees > 14:
            if self.document.wheel_flips_pages:
                self.previous_page()
                event.accept()
                return

            if self.document.at_top:
                if self.manager is not None:
                    self.manager.previous_document()
                    event.accept()
                    return

        ret = QWebView.wheelEvent(self, event)

        num_degrees_h = event.angleDelta().x() // 8
        vertical = abs(num_degrees) > abs(num_degrees_h)
        scroll_amount = ((num_degrees if vertical else num_degrees_h) / 120.0) * .2 * -1 * 8
        dim = self.document.viewportSize().height() if vertical else self.document.viewportSize().width()
        amt = dim * scroll_amount
        mult = -1 if amt < 0 else 1
        if self.document.wheel_scroll_fraction != 100:
            amt = mult * max(1, abs(int(amt * self.document.wheel_scroll_fraction / 100.)))
        self.scroll_by(0, amt) if vertical else self.scroll_by(amt, 0)

        if self.manager is not None:
            self.manager.scrolled(self.scroll_fraction)
        return ret

    def keyPressEvent(self, event):
        if not self.handle_key_press(event):
            return QWebView.keyPressEvent(self, event)

    def paged_col_scroll(self, forward=True, scroll_past_end=True):
        dir = 'next' if forward else 'previous'
        loc = self.document.javascript(
            'paged_display.%s_col_location()' % dir, typ='int')
        if loc > -1:
            self.document.scroll_to(x=loc, y=0)
            self.manager.scrolled(self.document.scroll_fraction)
        elif scroll_past_end:
            (self.manager.next_document() if forward else
             self.manager.previous_document())

    def handle_key_press(self, event):
        handled = True
        key = self.shortcuts.get_match(event)
        func = self.goto_location_actions.get(key, None)
        if func is not None:
            self.is_auto_repeat_event = event.isAutoRepeat()
            try:
                func()
            finally:
                self.is_auto_repeat_event = False
        elif key == 'Down':
            if self.document.in_paged_mode:
                self.paged_col_scroll(scroll_past_end=not
                self.document.line_scrolling_stops_on_pagebreaks)
            else:
                if (not self.document.line_scrolling_stops_on_pagebreaks and
                        self.document.at_bottom):
                    self.manager.next_document()
                else:
                    amt = int((self.document.line_scroll_fraction / 100.) * 15)
                    self.scroll_by(y=amt)
        elif key == 'Up':
            if self.document.in_paged_mode:
                self.paged_col_scroll(forward=False, scroll_past_end=not
                self.document.line_scrolling_stops_on_pagebreaks)
            else:
                if (not self.document.line_scrolling_stops_on_pagebreaks and
                        self.document.at_top):
                    self.manager.previous_document()
                else:
                    amt = int((self.document.line_scroll_fraction / 100.) * 15)
                    self.scroll_by(y=-amt)
        elif key == 'Left':
            if self.document.in_paged_mode:
                self.paged_col_scroll(forward=False)
            else:
                amt = int((self.document.line_scroll_fraction / 100.) * 15)
                self.scroll_by(x=-amt)
        elif key == 'Right':
            if self.document.in_paged_mode:
                self.paged_col_scroll()
            else:
                amt = int((self.document.line_scroll_fraction / 100.) * 15)
                self.scroll_by(x=amt)
        elif key == 'Back':
            if self.manager is not None:
                self.manager.back(None)
        elif key == 'Forward':
            if self.manager is not None:
                self.manager.forward(None)
        elif event.matches(QKeySequence.Copy):
            self.copy()
        else:
            handled = False
        return handled

    def resizeEvent(self, event):
        if self.manager is not None:
            self.manager.viewport_resize_started(event)
        return QWebView.resizeEvent(self, event)

    def event(self, ev):
        if self.gesture_handler(ev):
            return True
        return QWebView.event(self, ev)

    def mouseMoveEvent(self, ev):
        if self.document.in_paged_mode and ev.buttons() & Qt.LeftButton and not self.rect().contains(
                ev.pos(), True):
            # Prevent this event from causing WebKit to scroll the viewport
            # See https://bugs.launchpad.net/bugs/1464862
            return
        return QWebView.mouseMoveEvent(self, ev)

    def mouseReleaseEvent(self, ev):
        r = self.document.mainFrame().hitTestContent(ev.pos())
        a, url = r.linkElement(), r.linkUrl()
        if url.isValid() and not a.isNull() and self.manager is not None:
            fd = self.footnotes.get_footnote_data(a, url)
            if fd:
                self.footnotes.show_footnote(fd)
                self.manager.show_footnote_view()
                ev.accept()
                return
        opos = self.document.ypos
        if self.manager is not None:
            prev_pos = self.manager.update_page_number()
        ret = QWebView.mouseReleaseEvent(self, ev)
        if self.manager is not None and opos != self.document.ypos:
            self.manager.scrolled(self.scroll_fraction)
            self.manager.internal_link_clicked(prev_pos)
        return ret

    def follow_footnote_link(self):
        qurl = self.footnotes.showing_url
        if qurl and qurl.isValid():
            self.link_clicked(qurl)

    def set_book_data(self, iterator):
        self.document.nam.set_book_data(iterator.base, iterator.spine)
