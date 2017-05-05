# -*- coding: UTF-8 -*-
# !/usr/bin/env python2

from __future__ import (unicode_literals, division, absolute_import,
                        print_function)

import json
from base64 import b64decode, b64encode
from collections import defaultdict

from PyQt5.Qt import (
    QUrl, pyqtSlot)
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebPage, QWebView

from calibre import prints
from calibre.constants import DEBUG, FAKE_PROTOCOL, FAKE_HOST
from calibre.ebooks.oeb.display.webview import load_html
from calibre.gui2.viewer.qwebpage.qwebpage import Qwebpage
from calibre.gui2.viewer.qwebpage.qwebpageDocument import apply_basic_settings


class QwebpageFootnote(Qwebpage):
    def __init__(self, parent):
        QWebPage.__init__(self, parent)

        self.js_loader = None
        self._footnote_data = ''

        settings = self.settings()
        apply_basic_settings(settings)

        self.mainFrame().javaScriptWindowObjectCleared.connect(self.add_window_objects)
        self.add_window_objects()

    def add_window_objects(self, add_ready_listener=True):
        self.mainFrame().addToJavaScriptWindowObject("py_bridge", self)

        if self.js_loader is not None:
            evaljs = self.mainFrame().evaluateJavaScript
            for x in 'utils extract'.split():
                evaljs(self.js_loader.get(x))

    @pyqtSlot()
    def double_click(self):
        self.doubleClick.emit()

    @pyqtSlot(str)
    def debug(self, msg):
        prints(msg)

    @pyqtSlot(result=str)
    def footnote_data(self):
        return self._footnote_data

    def set_footnote_data(self, target, known_targets):
        self._footnote_data = json.dumps({'target': target, 'known_targets': known_targets})
        if self._footnote_data:
            self.mainFrame().evaluateJavaScript("""
data = JSON.parse(py_bridge.footnote_data());
calibre_extract.show_footnote(data["target"], data["known_targets"])
            """)

    def javaScriptAlert(self, frame, msg):
        prints('FootnoteView:alert::', msg)

    def javaScriptConsoleMessage(self, msg, lineno, source_id):
        if DEBUG:
            prints('FootnoteView:%s:%s:' % (unicode(source_id), lineno), unicode(msg))


class Footnotes(object):
    def __init__(self, view):
        self.f_qwebpage = None
        self.f_qwebview = None

        self.s_qwebview = view
        self.s_qwebpage = view.page()

        self.clear()

    def set_footnotes_view(self, fv):
        self.f_qwebview = fv.findChild(QWebView)
        self.f_qwebview.follow_link.connect(self.s_qwebview.follow_footnote_link)

        self.f_qwebpage = self.f_qwebview.page()
        self.f_qwebpage.linkClicked.connect(self.s_qwebview.link_clicked)
        self.f_qwebpage.js_loader = self.s_qwebpage.js_loader

        self.clone_settings()

    def clone_settings(self):
        s_settings = self.s_qwebpage.settings()
        f_settings = self.f_qwebpage.settings()
        for x in filter(lambda y: y.endswith(("FontSize", "Font")), QWebSettings.__dict__.keys()):
            name = 'setFontSize' if x.endswith('FontSize') else 'setFontFamily'

            try:
                value = getattr(s_settings, 'f' + name[4:])(getattr(QWebSettings, x))
            except TypeError:
                continue

            getattr(f_settings, name)(getattr(QWebSettings, x), value)

        raw = b64decode(
            s_settings.userStyleSheetUrl().toString().lstrip(
                "data:text/css;charset=utf-8;base64,"))
        raw += """
* {
    font-size: 15px !important;
    line-height: 28px !important;
}

body {
    margin: 0 11px !important;
}
        """
        data = 'data:text/css;charset=utf-8;base64,'
        data += b64encode(raw.encode('utf-8'))

        f_settings.setUserStyleSheetUrl(QUrl(data))

    def clear(self):
        self.known_footnote_targets = defaultdict(set)
        self.showing_url = None

    def spine_path(self, path):
        try:
            si = self.s_qwebview.manager.iterator.spine.index(path)
            return self.s_qwebview.manager.iterator.spine[si]
        except (AttributeError, ValueError):
            pass

    def get_footnote_data(self, a, qurl):
        current_path = self.s_qwebview.path()
        if not current_path:
            return  # Not viewing a local file

        dest_path = self.spine_path(self.s_qwebview.path(qurl))
        if dest_path is not None:
            if dest_path == current_path:
                # We deliberately ignore linked to anchors if the destination is
                # the same as the source, because many books have section ToCs
                # that are linked back from their destinations, for example,
                # the calibre User Manual
                linked_to_anchors = {}
            else:
                linked_to_anchors = {anchor: 0 for path, anchor in dest_path.verified_links if
                                     path == current_path}
            self.s_qwebpage.bridge_value = linked_to_anchors
            if a.evaluateJavaScript(
                    'calibre_extract.is_footnote_link(this, "{0}://{1}")'.format(
                        FAKE_PROTOCOL, FAKE_HOST)):
                if dest_path not in self.known_footnote_targets:
                    self.known_footnote_targets[dest_path] = s = set()
                    for item in self.s_qwebview.manager.iterator.spine:
                        for path, target in item.verified_links:
                            if target and path == dest_path:
                                s.add(target)

                return dest_path, qurl.fragment(QUrl.FullyDecoded), qurl

    def show_footnote(self, fd):
        path, target, self.showing_url = fd

        if hasattr(self, 'f_qwebview'):
            if load_html(
                    path, self.f_qwebview, codec=getattr(path, 'encoding', 'utf-8'),
                    mime_type=getattr(path, 'mime_type', 'text/html')):
                self.f_qwebpage.set_footnote_data(
                    target, {k: True for k in self.known_footnote_targets[path]})

                self.f_qwebview.show_parents()
