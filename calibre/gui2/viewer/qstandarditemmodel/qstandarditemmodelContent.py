# -*- coding: UTF-8 -*-

from __future__ import (unicode_literals, division, absolute_import, print_function)

from PyQt5.Qt import (QModelIndex)

from calibre.ebooks.metadata.toc import TOC as MTOC
from calibre.gui2.viewer.qstandarditem.qstandarditemContent import QstandarditemContent
from calibre.gui2.viewer.qstandarditemmodel.qstandarditemmodel import Qstandarditemmodel
from calibre.utils.icu import primary_contains

__license__ = 'GPL v3'
__copyright__ = '2012, Kovid Goyal <kovid@kovidgoyal.net>'
__docformat__ = 'restructuredtext en'

I = I
_ = _


class QstandarditemmodelContent(Qstandarditemmodel):
    def __init__(self, spine, toc=None, *args, **kwargs):
        super(QstandarditemmodelContent, self).__init__(*args, **kwargs)

        self.current_query = {'text': '', 'index': -1, 'items': ()}
        if toc is None:
            toc = MTOC()
        self.all_items = depth_first = []
        for t in toc:
            self.appendRow(QstandarditemContent(spine, t, 0, depth_first))

        for x in depth_first:
            possible_enders = [t for t in depth_first if t.depth <= x.depth and
                               t.starts_at >= x.starts_at and t is not x and t not in
                               x.ancestors]
            if possible_enders:
                min_spine = min(t.starts_at for t in possible_enders)
                possible_enders = {t.fragment for t in possible_enders if
                                   t.starts_at == min_spine}
            else:
                min_spine = len(spine) - 1
                possible_enders = set()
            x.ends_at = min_spine
            x.possible_end_anchors = possible_enders

        self.currently_viewed_entry = None

    def update_indexing_state(self, *args):
        items_being_viewed = []
        for t in self.all_items:
            t.update_indexing_state(*args)
            if t.is_being_viewed:
                items_being_viewed.append(t)
                self.currently_viewed_entry = t
        return items_being_viewed

    def next_entry(self, spine_pos, anchor_map, viewport_rect, in_paged_mode,
                   backwards=False, current_entry=None):
        current_entry = (self.currently_viewed_entry if current_entry is None
                         else current_entry)
        if current_entry is None:
            return
        items = reversed(self.all_items) if backwards else self.all_items
        found = False

        if in_paged_mode:
            start = viewport_rect[0]
            anchor_map = {k: v[0] for k, v in anchor_map.iteritems()}
        else:
            start = viewport_rect[1]
            anchor_map = {k: v[1] for k, v in anchor_map.iteritems()}

        for item in items:
            if found:
                start_pos = anchor_map.get(item.start_anchor, 0)
                if backwards and item.is_being_viewed and start_pos >= start:
                    # This item will not cause any scrolling
                    continue
                if item.starts_at != spine_pos or item.start_anchor:
                    return item
            if item is current_entry:
                found = True

    def find_items(self, query):
        for item in self.all_items:
            if primary_contains(query, item.text()):
                yield item

    def search(self, query):
        cq = self.current_query
        if cq['items'] and -1 < cq['index'] < len(cq['items']):
            cq['items'][cq['index']].set_current_search_result(False)
        if cq['text'] != query:
            items = tuple(self.find_items(query))
            cq.update({'text': query, 'items': items, 'index': -1})
        if len(cq['items']) > 0:
            cq['index'] = (cq['index'] + 1) % len(cq['items'])
            item = cq['items'][cq['index']]
            item.set_current_search_result(True)
            index = self.indexFromItem(item)
            return index
        return QModelIndex()

    @property
    def as_plain_text(self):
        lines = []
        for item in self.all_items:
            lines.append(' ' * (4 * item.depth) + (item.title or ''))
        return '\n'.join(lines)
