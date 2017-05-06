#!/usr/bin/env  python2
import math

from PyQt5.Qt import (QSize, QUrl, Qt, QPainter, QBrush, QImage, QRegion, QKeySequence)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWidgets import QMainWindow

from calibre.ebooks.oeb.display.webview import load_html
from calibre.gui2 import open_url, error_dialog
from calibre.gui2.viewer.qdialog.gestures import GestureHandler
from calibre.gui2.viewer.qdialog.qdialogConfig import config, load_themes
from calibre.gui2.viewer.qdialog.qdialogImage import ImagePopup
from calibre.gui2.viewer.qdialog.qdialogTablePopup import TablePopup
from calibre.gui2.viewer.qwebpage.qwebpageDocument import QwebpageDocument
from calibre.gui2.viewer.qwebpage.qwebpageFootnote import Footnotes
from calibre.gui2.viewer.qwebview.qwebview import Qwebview
from calibre.gui2.viewer.qwidget.qwidgetFootnote import QwidgetFootnote
from calibre.gui2.viewer.qwidget.qwidgetSlideFlip import QwidgetSlideFlip

__license__ = 'GPL v3'
__copyright__ = '2008, Kovid Goyal kovid@kovidgoyal.net'
__docformat__ = 'restructuredtext en'

_ = _
I = I
P = P
dynamic_property = dynamic_property


# todo
# - add synopsis insert through QdialogEdit
# - create QwidgetLookup for text lookup

class QwebviewDocument(Qwebview):
    DISABLED_BRUSH = QBrush(Qt.lightGray, Qt.Dense5Pattern)
    gesture_handler = lambda s, e: False
    last_loaded_path = None
    imageChanged = pyqtSignal(bool)
    tableChanged = pyqtSignal(bool)
    fontMultiplierUpdated = pyqtSignal(bool)
    copyChanged = pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super(QwebviewDocument, self).__init__(*args, **kwargs)

        self._context_blank_qactions = set()
        self._context_text_qactions = set()
        self._ignore_scrollbar_signals = False
        self._reference_mode = False
        self._size_hint = QSize(510, 680)
        self.goto_location_actions = {}
        self.initial_pos = 0.0
        self.is_auto_repeat_event = False
        self.loading_url = None
        self.manager = None
        self.to_bottom = False

        self.flipper = QwidgetSlideFlip(self)
        self.footnotes = Footnotes(self)
        self.gesture_handler = GestureHandler(self)
        self.image_popup = ImagePopup(self)
        self.table_popup = TablePopup(self)

        self.scrollbar = self.parent().horizontal_scrollbar
        self.scrollbar.valueChanged[(int)].connect(self.scroll_horizontally)

        self.loadFinished.connect(self.load_finished)
        self.qwebpage.settings_changed.connect(self.footnotes.clone_settings)
        self.create_actions(self.options["actions"])

        # fixme setMenu from Qobject
        self.qaction_synopsis.setMenu(self.qmenu_synopsis)
        self.qaction_search_online.setMenu(self.qmenu_search_online)
        self.qaction_goto_location.setMenu(self.qmenu_goto_location)

        self.qapplication.loadedUi.connect(self.on_qapplication_loadedUi)

        # This is needed for paged mode. Without it, the first document that is
        # loaded will have extra blank space at the bottom, as
        # turn_off_internal_scrollbars does not take effect for the first
        # rendered document
        self.load_path(P('viewer/blank.html', allow_user_override=False))

    def on_qapplication_loadedUi(self, qobject):
        if isinstance(qobject, QMainWindow):
            self.set_manager(qobject)

    def create_page(self):
        self.qwebpage = d = QwebpageDocument(self)
        d.nam.load_error.connect(self.on_unhandled_load_error)
        d.animated_scroll_done_signal.connect(self.animated_scroll_done, type=Qt.QueuedConnection)
        d.linkClicked.connect(self.link_clicked)
        d.linkHovered.connect(self.link_hovered)
        d.page_turn.connect(self.page_turn_requested)

        return d

    # ---- actions
    @property
    def context_blank_qactions(self):
        if not self.selected_text and self.image_popup.current_img.isNull():
            return self._context_blank_qactions
        return set()

    @property
    def context_text_qactions(self):
        if self.selected_text:
            return self._context_text_qactions
        return set()

    @property
    def context_qactions(self):
        return self.context_blank_qactions | self.context_text_qactions

    @property
    def mode_global_qaction(self):
        return True

    @property
    def pageAction_copy(self):
        return self.pageAction(self.qwebpage.Copy)

    @property
    def pageAction_inspect(self):
        return self.pageAction(self.qwebpage.InspectElement)

    def load_options(self, options):
        pass

    def addAction(self, qaction):
        super(QwebviewDocument, self).addAction(qaction)
        name = qaction.objectName()
        if name:
            setattr(self, name, qaction)

        data = qaction.data()
        if data:
            context = data.get("context", [])
            if "blank" in context:
                self._context_blank_qactions.add(qaction)
            if "text" in context:
                self._context_text_qactions.add(qaction)

    # --- markdown
    def copy_markdown(self, *args, **kwargs):
        data = self.sender().data()
        data["position"] = self.current_pos()

        self.qapplication.copy_markdown(data)

    def append_markdown(self, *args, **kwargs):
        data = self.sender().data()
        data["position"] = self.current_pos()

        self.qapplication.append_markdown(data)

    # --- position
    def current_pos(self):
        return self.qwebpage.page_position.current_pos if self.hasFocus() else None

    def copy_position(self):
        self.qapplication.copy_text(self.qwebpage.page_position.current_pos)

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
        self.qwebpage.goto(ref)

    def goto_bookmark(self, bm):
        self.qwebpage.goto_bookmark(bm)

    # ---
    def animated_scroll_done(self):
        if self.manager is not None:
            self.manager.scrolled(self.qwebpage.scroll_fraction)

    def reference_mode(self, enable):
        self._reference_mode = enable
        self.qwebpage.reference_mode(enable)

    def config(self, parent=None):
        self.qwebpage.do_config(parent)
        if self.qwebpage.in_fullscreen_mode:
            self.qwebpage.switch_to_fullscreen_mode()

        self.setFocus(Qt.OtherFocusReason)

    def load_theme(self, theme_id):
        themes = load_themes()
        theme = themes[theme_id]
        opts = config(theme).parse()
        self.qwebpage.apply_settings(opts)
        if self.qwebpage.in_fullscreen_mode:
            self.qwebpage.switch_to_fullscreen_mode()
        self.setFocus(Qt.OtherFocusReason)

    def bookmark(self):
        return self.qwebpage.bookmark()

    def popup_table(self):
        html = self.qwebpage.extract_node()
        self.table_popup(html, self.as_url(self.last_loaded_path),
                         self.qwebpage.font_magnification_step)

    def set_table(self, qwebhittestresult):
        table = None
        if not qwebhittestresult.element().isNull():
            parent = qwebhittestresult.element()
        else:
            parent = qwebhittestresult.enclosingBlockElement()
        while not parent.isNull():
            if u'table' in [unicode(parent.tagName()), unicode(parent.localName())]:
                table = parent
                break
            parent = parent.parent()

        if table is not None:
            self.qwebpage.mark_element.emit(table)

        self.tableChanged.emit(table is not None)

    def set_image(self, qwebhittestresult):
        self.image_popup.current_img = i = qwebhittestresult.pixmap()
        self.image_popup.current_url = qwebhittestresult.imageUrl()

        self.imageChanged.emit(not i.isNull())

    def contextMenuEvent(self, qevent):
        q = self.qwebpage.mainFrame().hitTestContent(qevent.pos())

        self.set_image(q)
        self.set_table(q)
        self.fontMultiplierUpdated.emit(self.multiplier == 1)

        menu = self.page().createStandardContextMenu()
        menu.addActions(self.context_qactions)

        if not menu.exec_(qevent.globalPos()):
            super(QwebviewDocument, self).contextMenuEvent(qevent)

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
        qwidget = self.qapplication.focusWidget()
        t = unicode(getattr(qwidget, "selected_text")).strip()
        if t:
            self.open_url(t, self.sender().data().get("url", None))

    def open_url(self, text, url):
        if url:
            url = url.replace('%s', QUrl().toPercentEncoding(text))
        if not isinstance(url, bytes):
            url = url.encode('utf-8')

        open_url(QUrl.fromEncoded(url))

    def set_manager(self, manager):
        self.manager = manager
        self.manager.start_in_fullscreen = self.qwebpage.start_in_fullscreen
        self.manager.iteratorChanged.connect(self.set_book_data)

        self.qwebpage.debug_javascript = self.manager.debug_javascript
        self.footnotes.set_footnotes_view(self.manager.findChild(QwidgetFootnote))

        map(lambda p: p.customize_ui(self.manager), self.qwebpage.all_viewer_plugins)

    def scroll_horizontally(self, amount):
        self.qwebpage.scroll_to(y=self.qwebpage.ypos, x=amount)

    @property
    def scroll_pos(self):
        return (self.qwebpage.ypos, self.qwebpage.ypos +
                self.qwebpage.window_height)

    @property
    def viewport_rect(self):
        # (left, top, right, bottom) of the viewport in document co-ordinates
        # When in paged mode, left and right are the numbers of the columns
        # at the left edge and *after* the right edge of the viewport
        d = self.qwebpage
        if d.in_paged_mode:
            try:
                l, r = d.column_boundaries
            except ValueError:
                l, r = (0, 1)
        else:
            l, r = d.xpos, d.xpos + d.window_width
        return l, d.ypos, r, d.ypos + d.window_height

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
            return self.qwebpage.scroll_fraction

        def fset(self, val):
            self.qwebpage.scroll_fraction = float(val)

        return property(fget=fget, fset=fset)

    @property
    def hscroll_fraction(self):
        return self.qwebpage.hscroll_fraction

    @property
    def content_size(self):
        return self.qwebpage.width, self.qwebpage.height

    @dynamic_property
    def current_language(self):
        def fget(self):
            return self.qwebpage.current_language

        def fset(self, val):
            self.qwebpage.current_language = val

        return property(fget=fget, fset=fset)

    def search(self, text, backwards=False):
        flags = self.qwebpage.FindBackward if backwards else self.qwebpage.FindFlags(0)
        found = self.qwebpage.findText(text, flags)
        if found and self.qwebpage.in_paged_mode:
            self.qwebpage.javascript('paged_display.snap_to_selection()')
        return found

    def path(self, url=None):
        url = url or self.url()
        return self.qwebpage.nam.as_abspath(url)

    def as_url(self, path):
        return self.qwebpage.nam.as_url(path)

    def load_path(self, path, pos=0.0):
        self.initial_pos = pos
        self.last_loaded_path = path
        # This is needed otherwise percentage margins on body are not correctly
        # evaluated in read_document_margins() in paged mode.
        self.qwebpage.setPreferredContentsSize(QSize())

        url = self.as_url(path)
        entries = set()
        for ie in getattr(path, 'index_entries', []):
            if ie.start_anchor:
                entries.add(ie.start_anchor)
            if ie.end_anchor:
                entries.add(ie.end_anchor)
        self.qwebpage.index_anchors = entries

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
            if self.qwebpage.in_paged_mode:
                self.scrollbar.setVisible(False)
                return
            delta = self.qwebpage.width - self.size().width()
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
        self.qwebpage.load_javascript_libraries()
        self.qwebpage.after_load(self.last_loaded_path)
        self._size_hint = self.qwebpage.mainFrame().contentsSize()
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
        self.qwebpage.reference_mode(self._reference_mode)
        if self.manager is not None:
            spine_index = self.manager.load_finished(bool(ok))
            if spine_index > -1:
                self.qwebpage.set_reference_prefix('%d.' % (spine_index + 1))
            if scrolled:
                self.manager.scrolled(self.qwebpage.scroll_fraction,
                                      onload=True)

        if self.flipper.isVisible():
            if self.flipper.running:
                self.flipper.setVisible(False)
            else:
                self.flipper(self.current_page_image(),
                             duration=self.qwebpage.page_flip_duration)

    @classmethod
    def test_line(cls, img, y):
        """Test if line contains pixels of exactly the same color"""
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
        self.qwebpage.mainFrame().render(painter, QRegion(0, 0, self.width(), overlap))
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
        epf = self.qwebpage.enable_page_flip and not self.is_auto_repeat_event

        if self.qwebpage.in_paged_mode:
            loc = self.qwebpage.javascript(
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
                self.qwebpage.scroll_to(x=loc, y=0)
                if epf:
                    self.flipper(self.current_page_image(),
                                 duration=self.qwebpage.page_flip_duration)
                if self.manager is not None:
                    self.manager.scrolled(self.scroll_fraction)

            return

        delta_y = self.qwebpage.window_height - 25
        if self.qwebpage.at_top:
            if self.manager is not None:
                self.to_bottom = True
                if epf:
                    self.flipper.initialize(self.current_page_image(), False)
                self.manager.previous_document()
        else:
            opos = self.qwebpage.ypos
            upper_limit = opos - delta_y
            if upper_limit < 0:
                upper_limit = 0
            if upper_limit < opos:
                if epf:
                    self.flipper.initialize(self.current_page_image(),
                                            forwards=False)
                self.qwebpage.scroll_to(self.qwebpage.xpos, upper_limit)
                if epf:
                    self.flipper(self.current_page_image(),
                                 duration=self.qwebpage.page_flip_duration)
                if self.manager is not None:
                    self.manager.scrolled(self.scroll_fraction)

    def next_page(self):
        if self.flipper.running and not self.is_auto_repeat_event:
            return
        if self.loading_url is not None:
            return
        epf = self.qwebpage.enable_page_flip and not self.is_auto_repeat_event

        if self.qwebpage.in_paged_mode:
            loc = self.qwebpage.javascript(
                'paged_display.next_screen_location()', typ='int')
            if loc < 0:
                if self.manager is not None:
                    if epf:
                        self.flipper.initialize(self.current_page_image())
                    self.manager.next_document()
            else:
                if epf:
                    self.flipper.initialize(self.current_page_image())
                self.qwebpage.scroll_to(x=loc, y=0)
                if epf:
                    self.flipper(self.current_page_image(),
                                 duration=self.qwebpage.page_flip_duration)
                if self.manager is not None:
                    self.manager.scrolled(self.scroll_fraction)

            return

        window_height = self.qwebpage.window_height
        document_height = self.qwebpage.height
        ddelta = document_height - window_height

        delta_y = window_height - 25
        if self.qwebpage.at_bottom or ddelta <= 0:
            if self.manager is not None:
                if epf:
                    self.flipper.initialize(self.current_page_image())
                self.manager.next_document()
        elif ddelta < 25:
            self.scroll_by(y=ddelta)
            return
        else:
            oopos = self.qwebpage.ypos
            self.qwebpage.set_bottom_padding(0)
            opos = self.qwebpage.ypos
            if opos < oopos:
                if self.manager is not None:
                    if epf:
                        self.flipper.initialize(self.current_page_image())
                    self.manager.next_document()
                return
            lower_limit = opos + delta_y  # Max value of top y co-ord after scrolling
            max_y = self.qwebpage.height - window_height  # The maximum possible top y co-ord
            if max_y < lower_limit:
                padding = lower_limit - max_y
                if padding == window_height:
                    if self.manager is not None:
                        if epf:
                            self.flipper.initialize(self.current_page_image())
                        self.manager.next_document()
                    return
                self.qwebpage.set_bottom_padding(lower_limit - max_y)
            if epf:
                self.flipper.initialize(self.current_page_image())
            max_y = self.qwebpage.height - window_height
            lower_limit = min(max_y, lower_limit)
            if lower_limit > opos:
                self.qwebpage.scroll_to(self.qwebpage.xpos, lower_limit)
            actually_scrolled = self.qwebpage.ypos - opos
            self.find_next_blank_line(window_height - actually_scrolled)
            if epf:
                self.flipper(self.current_page_image(),
                             duration=self.qwebpage.page_flip_duration)
            if self.manager is not None:
                self.manager.scrolled(self.scroll_fraction)

    def page_turn_requested(self, backwards):
        if backwards:
            self.previous_page()
        else:
            self.next_page()

    def scroll_by(self, x=0, y=0, notify=True):
        old_pos = (self.qwebpage.xpos if self.qwebpage.in_paged_mode else
                   self.qwebpage.ypos)
        self.qwebpage.scroll_by(x, y)
        new_pos = (self.qwebpage.xpos if self.qwebpage.in_paged_mode else
                   self.qwebpage.ypos)
        if notify and self.manager is not None and new_pos != old_pos:
            self.manager.scrolled(self.scroll_fraction)

    def scroll_to(self, pos, notify=True):
        if self._ignore_scrollbar_signals:
            return
        old_pos = (self.qwebpage.xpos if self.qwebpage.in_paged_mode else
                   self.qwebpage.ypos)
        if self.qwebpage.in_paged_mode:
            if isinstance(pos, basestring):
                self.qwebpage.jump_to_anchor(pos)
            else:
                self.qwebpage.scroll_fraction = pos
        else:
            if isinstance(pos, basestring):
                self.qwebpage.jump_to_anchor(pos)
            else:
                if pos >= 1:
                    self.qwebpage.scroll_to(0, self.qwebpage.height)
                else:
                    y = int(math.ceil(
                        pos * (self.qwebpage.height - self.qwebpage.window_height)))
                    self.qwebpage.scroll_to(0, y)

        new_pos = (self.qwebpage.xpos if self.qwebpage.in_paged_mode else
                   self.qwebpage.ypos)
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
                if self.qwebpage.in_paged_mode:
                    self.qwebpage.update_contents_size_for_paged_mode()

                self.update_font(val)

        return property(fget=fget, fset=fset)

    def update_font(self, val):
        tt = '%(action)s [%(sc)s]\n' + _('Current magnification: %(mag).1f')
        sc = _(' or ').join(
            self.qapplication.qabstractlistmodelShortcut.get_shortcuts('Font larger'))
        self.qaction_font_size_larger.setToolTip(
            tt % dict(action=unicode(self.qaction_font_size_larger.text()), mag=val, sc=sc))
        sc = _(' or ').join(
            self.qapplication.qabstractlistmodelShortcut.get_shortcuts('Font smaller'))
        self.qaction_font_size_smaller.setToolTip(
            tt % dict(action=unicode(self.qaction_font_size_smaller.text()), mag=val, sc=sc))
        self.qaction_font_size_larger.setEnabled(self.view.multiplier < 3)
        self.qaction_font_size_smaller.setEnabled(self.view.multiplier > 0.2)

    def magnify_fonts(self, amount=None):
        if amount is None:
            amount = self.qwebpage.font_magnification_step
        with self.qwebpage.page_position:
            self.multiplier += amount
        return self.qwebpage.scroll_fraction

    def shrink_fonts(self, amount=None):
        if amount is None:
            amount = self.qwebpage.font_magnification_step
        if self.multiplier >= amount:
            with self.qwebpage.page_position:
                self.multiplier -= amount
        return self.qwebpage.scroll_fraction

    def restore_font_size(self):
        with self.qwebpage.page_position:
            self.multiplier = 1

        return self.qwebpage.scroll_fraction

    def changeEvent(self, event):
        if event.type() == event.EnabledChange:
            self.update()
        return QWebView.changeEvent(self, event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHints(self.renderHints())
        self.qwebpage.mainFrame().render(painter, event.region())
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
                (self.magnify_fonts if num_degrees > 0 else
                 self.shrink_fonts)()
                return

        if self.qwebpage.in_paged_mode:
            if abs(num_degrees) < 15:
                return
            typ = 'screen' if self.qwebpage.wheel_flips_pages else 'col'
            direction = 'next' if num_degrees < 0 else 'previous'
            loc = self.qwebpage.javascript('paged_display.%s_%s_location()' % (
                direction, typ), typ='int')
            if loc > -1:
                self.qwebpage.scroll_to(x=loc, y=0)
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
            if self.qwebpage.wheel_flips_pages:
                self.next_page()
                event.accept()
                return
            if self.qwebpage.at_bottom:
                self.scroll_by(y=15)  # at_bottom can lie on windows
                if self.manager is not None:
                    self.manager.next_document()
                    event.accept()
                    return
        elif num_degrees > 14:
            if self.qwebpage.wheel_flips_pages:
                self.previous_page()
                event.accept()
                return

            if self.qwebpage.at_top:
                if self.manager is not None:
                    self.manager.previous_document()
                    event.accept()
                    return

        ret = QWebView.wheelEvent(self, event)

        num_degrees_h = event.angleDelta().x() // 8
        vertical = abs(num_degrees) > abs(num_degrees_h)
        scroll_amount = ((num_degrees if vertical else num_degrees_h) / 120.0) * .2 * -1 * 8
        dim = self.qwebpage.viewportSize().height() if vertical else self.qwebpage.viewportSize().width()
        amt = dim * scroll_amount
        mult = -1 if amt < 0 else 1
        if self.qwebpage.wheel_scroll_fraction != 100:
            amt = mult * max(1, abs(int(amt * self.qwebpage.wheel_scroll_fraction / 100.)))
        self.scroll_by(0, amt) if vertical else self.scroll_by(amt, 0)

        if self.manager is not None:
            self.manager.scrolled(self.scroll_fraction)
        return ret

    def keyPressEvent(self, event):
        if not self.handle_key_press(event):
            return QWebView.keyPressEvent(self, event)

    def paged_col_scroll(self, forward=True, scroll_past_end=True):
        dir = 'next' if forward else 'previous'
        loc = self.qwebpage.javascript(
            'paged_display.%s_col_location()' % dir, typ='int')
        if loc > -1:
            self.qwebpage.scroll_to(x=loc, y=0)
            self.manager.scrolled(self.qwebpage.scroll_fraction)
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
            if self.qwebpage.in_paged_mode:
                self.paged_col_scroll(
                    scroll_past_end=not self.qwebpage.line_scrolling_stops_on_pagebreaks)
            else:
                if (not self.qwebpage.line_scrolling_stops_on_pagebreaks and
                        self.qwebpage.at_bottom):
                    self.manager.next_document()
                else:
                    amt = int((self.qwebpage.line_scroll_fraction / 100.) * 15)
                    self.scroll_by(y=amt)
        elif key == 'Up':
            if self.qwebpage.in_paged_mode:
                self.paged_col_scroll(
                    forward=False,
                    scroll_past_end=not self.qwebpage.line_scrolling_stops_on_pagebreaks)
            else:
                if (not self.qwebpage.line_scrolling_stops_on_pagebreaks and
                        self.qwebpage.at_top):
                    self.manager.previous_document()
                else:
                    amt = int((self.qwebpage.line_scroll_fraction / 100.) * 15)
                    self.scroll_by(y=-amt)
        elif key == 'Left':
            if self.qwebpage.in_paged_mode:
                self.paged_col_scroll(forward=False)
            else:
                amt = int((self.qwebpage.line_scroll_fraction / 100.) * 15)
                self.scroll_by(x=-amt)
        elif key == 'Right':
            if self.qwebpage.in_paged_mode:
                self.paged_col_scroll()
            else:
                amt = int((self.qwebpage.line_scroll_fraction / 100.) * 15)
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
        if self.qwebpage.in_paged_mode and ev.buttons() & Qt.LeftButton and not self.rect().contains(
                ev.pos(), True):
            # Prevent this event from causing WebKit to scroll the viewport
            # See https://bugs.launchpad.net/bugs/1464862
            return
        return QWebView.mouseMoveEvent(self, ev)

    def mouseReleaseEvent(self, ev):
        r = self.qwebpage.mainFrame().hitTestContent(ev.pos())
        a, url = r.linkElement(), r.linkUrl()
        if url.isValid() and not a.isNull() and self.manager is not None:
            fd = self.footnotes.get_footnote_data(a, url)
            if fd:
                self.footnotes.show_footnote(fd)
                ev.accept()
                return
        opos = self.qwebpage.ypos
        if self.manager is not None:
            prev_pos = self.manager.update_page_number()
        ret = QWebView.mouseReleaseEvent(self, ev)
        if self.manager is not None and opos != self.qwebpage.ypos:
            self.manager.scrolled(self.scroll_fraction)
            self.manager.internal_link_clicked(prev_pos)
        return ret

    def follow_footnote_link(self):
        qurl = self.footnotes.showing_url
        if qurl and qurl.isValid():
            self.link_clicked(qurl)

    def set_book_data(self, iterator):
        self.qwebpage.current_language = iterator.language
        self.qwebpage.nam.set_book_data(iterator.base, iterator.spine)
