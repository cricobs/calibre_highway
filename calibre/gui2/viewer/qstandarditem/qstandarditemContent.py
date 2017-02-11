# -*- coding: UTF-8 -*-

import re

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem, QFont


class QstandarditemContent(QStandardItem):
    def __init__(self, spine, toc, depth, all_items, parent=None):
        text = toc.text
        if text:
            text = re.sub(r'\s', ' ', text)
        self.title = text
        self.parent = parent
        QStandardItem.__init__(self, text if text else '')
        self.abspath = toc.abspath if toc.href else None
        self.fragment = toc.fragment
        all_items.append(self)
        self.emphasis_font = QFont(self.font())
        self.emphasis_font.setBold(True), self.emphasis_font.setItalic(True)
        self.normal_font = self.font()
        for t in toc:
            self.appendRow(QstandarditemContent(spine, t, depth + 1, all_items, parent=self))
        self.setFlags(Qt.ItemIsEnabled)
        self.is_current_search_result = False
        spos = 0
        for i, si in enumerate(spine):
            if si == self.abspath:
                spos = i
                break
        am = {}
        if self.abspath is not None:
            try:
                am = getattr(spine[i], 'anchor_map', {})
            except UnboundLocalError:
                # Spine was empty?
                pass
        frag = self.fragment if (self.fragment and self.fragment in am) else None
        self.starts_at = spos
        self.start_anchor = frag
        self.start_src_offset = am.get(frag, 0)
        self.depth = depth
        self.is_being_viewed = False

    @property
    def ancestors(self):
        parent = self.parent
        while parent is not None:
            yield parent
            parent = parent.parent

    @classmethod
    def type(cls):
        return QStandardItem.UserType + 10

    def update_indexing_state(self, spine_index, viewport_rect, anchor_map,
                              in_paged_mode):
        if in_paged_mode:
            self.update_indexing_state_paged(spine_index, viewport_rect,
                                             anchor_map)
        else:
            self.update_indexing_state_unpaged(spine_index, viewport_rect,
                                               anchor_map)

    def update_indexing_state_unpaged(self, spine_index, viewport_rect,
                                      anchor_map):
        is_being_viewed = False
        top, bottom = viewport_rect[1], viewport_rect[3]
        # We use bottom-25 in the checks below to account for the case where
        # the next entry has some invisible margin that just overlaps with the
        # bottom of the screen. In this case it will appear to the user that
        # the entry is not visible on the screen. Of course, the margin could
        # be larger than 25, but that's a decent compromise. Also we dont want
        # to count a partial line as being visible.

        # We only care about y position
        anchor_map = {k: v[1] for k, v in anchor_map.iteritems()}

        if spine_index >= self.starts_at and spine_index <= self.ends_at:
            # The position at which this anchor is present in the document
            start_pos = anchor_map.get(self.start_anchor, 0)
            psp = []
            if self.ends_at == spine_index:
                # Anchors that could possibly indicate the start of the next
                # section and therefore the end of this section.
                # self.possible_end_anchors is a set of anchors belonging to
                # toc entries with depth <= self.depth that are also not
                # ancestors of this entry.
                psp = [anchor_map.get(x, 0) for x in self.possible_end_anchors]
                psp = [x for x in psp if x >= start_pos]
            # The end position. The first anchor whose pos is >= start_pos
            # or if the end is not in this spine item, we set it to the bottom
            # of the window +1
            end_pos = min(psp) if psp else (bottom + 1 if self.ends_at >=
                                                          spine_index else 0)
            if spine_index > self.starts_at and spine_index < self.ends_at:
                # The entire spine item is contained in this entry
                is_being_viewed = True
            elif (spine_index == self.starts_at and bottom - 25 >= start_pos and
                  # This spine item contains the start
                  # The start position is before the end of the viewport
                      (spine_index != self.ends_at or top < end_pos)):
                # The end position is after the start of the viewport
                is_being_viewed = True
            elif (spine_index == self.ends_at and top < end_pos and
                  # This spine item contains the end
                  # The end position is after the start of the viewport
                      (spine_index != self.starts_at or bottom - 25 >= start_pos)):
                # The start position is before the end of the viewport
                is_being_viewed = True

        changed = is_being_viewed != self.is_being_viewed
        self.is_being_viewed = is_being_viewed
        if changed:
            self.setFont(self.emphasis_font if is_being_viewed else self.normal_font)

    def update_indexing_state_paged(self, spine_index, viewport_rect,
                                    anchor_map):
        is_being_viewed = False

        left, right = viewport_rect[0], viewport_rect[2]
        left, right = (left, 0), (right, -1)

        if spine_index >= self.starts_at and spine_index <= self.ends_at:
            # The position at which this anchor is present in the document
            start_pos = anchor_map.get(self.start_anchor, (0, 0))
            psp = []
            if self.ends_at == spine_index:
                # Anchors that could possibly indicate the start of the next
                # section and therefore the end of this section.
                # self.possible_end_anchors is a set of anchors belonging to
                # toc entries with depth <= self.depth that are also not
                # ancestors of this entry.
                psp = [anchor_map.get(x, (0, 0)) for x in self.possible_end_anchors]
                psp = [x for x in psp if x >= start_pos]
            # The end position. The first anchor whose pos is >= start_pos
            # or if the end is not in this spine item, we set it to the column
            # after the right edge of the viewport
            end_pos = min(psp) if psp else (right if self.ends_at >=
                                                     spine_index else (0, 0))
            if spine_index > self.starts_at and spine_index < self.ends_at:
                # The entire spine item is contained in this entry
                is_being_viewed = True
            elif (spine_index == self.starts_at and right > start_pos and
                  # This spine item contains the start
                  # The start position is before the end of the viewport
                      (spine_index != self.ends_at or left < end_pos)):
                # The end position is after the start of the viewport
                is_being_viewed = True
            elif (spine_index == self.ends_at and left < end_pos and
                  # This spine item contains the end
                  # The end position is after the start of the viewport
                      (spine_index != self.starts_at or right > start_pos)):
                # The start position is before the end of the viewport
                is_being_viewed = True

        changed = is_being_viewed != self.is_being_viewed
        self.is_being_viewed = is_being_viewed
        if changed:
            self.setFont(self.emphasis_font if is_being_viewed else self.normal_font)

    def set_current_search_result(self, yes):
        if yes and not self.is_current_search_result:
            self.setText(self.text() + ' ◄')
            self.is_current_search_result = True
        elif not yes and self.is_current_search_result:
            self.setText(self.text()[:-2])
            self.is_current_search_result = False

    def __repr__(self):
        return 'QstandarditemmodelContent Item: %s %s#%s' % (
        self.title, self.abspath, self.fragment)

    def __str__(self):
        return repr(self)