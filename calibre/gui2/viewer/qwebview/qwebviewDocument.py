#!/usr/bin/env  python2

import math

from PyQt5.Qt import (QSize, QUrl, Qt, QPainter, QBrush, QImage, QRegion, pyqtSignal, QApplication,
                      QKeySequence, QMimeData)
from PyQt5.QtWebKitWidgets import QWebView

from calibre.constants import iswindows
from calibre.ebooks.oeb.display.webview import load_html
from calibre.gui2 import open_url, error_dialog
from calibre.gui2.viewer.qdialog.gestures import GestureHandler
from calibre.gui2.viewer.qdialog.qdialogConfig import config, load_themes
from calibre.gui2.viewer.qdialog.qdialogImage import ImagePopup
from calibre.gui2.viewer.qdialog.qdialogTablePopup import TablePopup
from calibre.gui2.viewer.qwebpage.qwebpageDocument import Document
from calibre.gui2.viewer.qwebpage.qwebpageFootnote import Footnotes
from calibre.gui2.viewer.qwebview.qwebview import Qwebview
from calibre.gui2.viewer.qwidget.qwidgetSlideFlip import QwidgetSlideFlip

__license__ = 'GPL v3'
__copyright__ = '2008, Kovid Goyal kovid@kovidgoyal.net'
__docformat__ = 'restructuredtext en'

_ = _
I = I
dynamic_property = dynamic_property


# todo
# - replace synopsis insert actions for QdialogEdit

class QwebviewDocument(Qwebview):
    magnification_changed = pyqtSignal(object)
    DISABLED_BRUSH = QBrush(Qt.lightGray, Qt.Dense5Pattern)
    gesture_handler = lambda s, e: False
    last_loaded_path = None

    def __init__(self, *args, **kwargs):
        super(QwebviewDocument, self).__init__(*args, **kwargs)

        self._qaction_copy = None
        self._qaction_inspect = None
        self._context_blank_qactions = set()

    @property
    def context_blank_qactions(self):
        if not self.selected_text and self.image_popup.current_img.isNull():
            return self._context_blank_qactions
        return []

    def set_footnotes_view(self, view):
        self.footnotes.set_footnotes_view(view)
        view.follow_link.connect(self.follow_footnote_link)

    @property
    def mode_search(self):
        return self.SEARCH

    def initialize_view(self, debug_javascript=False):
        self._ignore_scrollbar_signals = False
        self._reference_mode = False
        self._size_hint = QSize(510, 680)
        self.debug_javascript = debug_javascript
        self.flipper = QwidgetSlideFlip(self)
        self.footnotes = Footnotes(self)
        self.gesture_handler = GestureHandler(self)
        self.goto_location_actions = {}
        self.image_popup = ImagePopup(self)
        self.initial_pos = 0.0
        self.is_auto_repeat_event = False
        self.loading_url = None
        self.manager = None
        self.table_popup = TablePopup(self)
        self.to_bottom = False

        self.document = d = Document(
            self.qapplication.qabstractlistmodelShortcut, parent=self,
            debug_javascript=debug_javascript)
        d.nam.load_error.connect(self.on_unhandled_load_error)
        d.settings_changed.connect(self.footnotes.clone_settings)
        d.animated_scroll_done_signal.connect(self.animated_scroll_done, type=Qt.QueuedConnection)
        d.linkClicked.connect(self.link_clicked)
        d.linkHovered.connect(self.link_hovered)
        d.page_turn.connect(self.page_turn_requested)
        d.selectionChanged[()].connect(self.selection_changed)

        self.loadFinished.connect(self.load_finished)
        self.setPage(d)

        self.create_actions(self.options["actions"])

        self.qaction_synopsis.setMenu(self.qmenu_synopsis)
        self.qaction_search_online.setMenu(self.qmenu_search_online)
        self.qaction_goto_location.setMenu(self.qmenu_goto_location)

    @property
    def mode_qapplication_qaction(self):
        return True

    # ---- actions
    @property
    def pageAction_copy(self):
        return self.pageAction(self.document.Copy)

    @property
    def pageAction_inspect(self):
        return self.pageAction(self.document.InspectElement)

    def load_options(self, options):
        pass

    def addAction(self, qaction):
        super(QwebviewDocument, self).addAction(qaction)
        name = qaction.objectName()
        if name:
            setattr(self, name, qaction)

        data = qaction.data()
        if data and data.get("context", None) == "blank":
            self.context_blank_qactions.add(qaction)

    # --- synopsis
    def copy_markdown(self, *args, **kwargs):
        self.copy_text(self.selected_markdown_body())

    def synopsis_append(self, *args, **kwargs):
        section = self.sender().data().get("section")
        position = self.document.page_position.current_pos
        if section == "body":
            text = self.selected_markdown_body(position)
        elif section == "header":
            text = self.selected_markdown_header(int(self.sender().text()), position)
        else:
            raise NotImplementedError(section)

        if text:
            self.manager.qdockwidgetSynopsis.qstackedwidgetSynopsis.append(text, position)

    def selected_markdown_header(self, level, position=None):
        if self.selected_text:
            position = position if position else self.document.page_position.current_pos
            return "\n{0} <a class='header' position='{1}'>{2}</a>".format(
                "#" * level, position, self.selected_text)

    def selected_markdown_body(self, position=None):
        if self.selected_text:
            position = position if position else self.document.page_position.current_pos
            return "\n{0}\n{{: position={1}}}".format(self.selected_text, position)

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

    # ---
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

    def popup_table(self):
        html = self.document.extract_node()
        self.table_popup(html, self.as_url(self.last_loaded_path),
                         self.document.font_magnification_step)

    def contextMenuEvent(self, qevent):
        r = self.document.mainFrame().hitTestContent(qevent.pos())

        self.image_popup.current_img = img = r.pixmap()
        self.image_popup.current_url = r.imageUrl()

        table = None
        parent = r.element() if not r.element().isNull() else r.enclosingBlockElement()
        while not parent.isNull():
            if u'table' in [unicode(parent.tagName()), unicode(parent.localName())]:
                table = parent
                break
            parent = parent.parent()

        if table is not None:
            self.document.mark_element.emit(table)

        self.qaction_view_image.setEnabled(not img.isNull())
        self.qaction_view_table.setEnabled(table is not None)
        self.qaction_restore_fonts.setChecked(self.multiplier == 1)

        menu = self.document.createStandardContextMenu()
        menu.addActions(self.context_blank_qactions)
        menu.addAction(self.qaction_inspect)

        for plugin in self.document.all_viewer_plugins:
            plugin.customize_context_menu(menu, qevent, r)

        menu.exec_(qevent.globalPos())

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
        url = action.data().get("url", None)
        if url:
            url = url.replace('%s', QUrl().toPercentEncoding(text))
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

        load_html(
            path, self, codec=getattr(path, 'encoding', 'utf-8'),
            mime_type=getattr(path, 'mime_type', 'text/html'), loading_url=url,
            pre_load_callback=callback)

    def on_unhandled_load_error(self, name, tb):
        error_dialog(
            self, _('Failed to load file'),
            _('Failed to load the file: {}. Click "Show details" for more information').format(
                name), det_msg=tb, show=True)

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
            self.document.set_bottom_padding(0)
            opos = self.document.ypos
            if opos < oopos:
                if self.manager is not None:
                    if epf:
                        self.flipper.initialize(self.current_page_image())
                    self.manager.next_document()
                return
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
                self.document.set_bottom_padding(lower_limit - max_y)
            if epf:
                self.flipper.initialize(self.current_page_image())
            max_y = self.document.height - window_height
            lower_limit = min(max_y, lower_limit)
            if lower_limit > opos:
                self.document.scroll_to(self.document.xpos, lower_limit)
            actually_scrolled = self.document.ypos - opos
            self.find_next_blank_line(window_height - actually_scrolled)
            if epf:
                self.flipper(self.current_page_image(),
                             duration=self.document.page_flip_duration)
            if self.manager is not None:
                self.manager.scrolled(self.scroll_fraction)

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
        key = self.qapplication.qabstractlistmodelShortcut.get_match(event)
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
