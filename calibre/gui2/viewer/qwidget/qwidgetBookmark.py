from __future__ import (unicode_literals, division, absolute_import, print_function)

import cPickle

from PyQt5.Qt import (Qt, QListWidgetItem, QItemSelectionModel, QIcon, pyqtSignal)
from PyQt5.QtCore import pyqtSlot

from calibre.gui2 import choose_save_file, choose_files
from calibre.gui2.viewer.qwidget.qwidget import Qwidget
from calibre.utils.icu import sort_key

_ = _
I = I


class QwidgetBookmark(Qwidget):
    edited = pyqtSignal(object)
    activated = pyqtSignal(object)
    create_requested = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(QwidgetBookmark, self).__init__(*args, **kwargs)
        self.sorted = False

        bl = self.bookmarks_list
        bl.itemChanged.connect(self.item_changed)
        bl.itemClicked.connect(self.item_activated)
        bl.bookmark_activated.connect(self.item_activated)
        bl.changed.connect(lambda: self.edited.emit(self.get_bookmarks()))
        bl.ac_edit.triggered.connect(self.edit_bookmark)
        bl.ac_sort.triggered.connect(self.sort_by_name)
        bl.ac_sort_pos.triggered.connect(self.sort_by_pos)
        bl.ac_delete.triggered.connect(self.delete_bookmark)

        self.toolButton_new.setIcon(QIcon(I('bookmarks.png')))
        self.toolButton_new.clicked.connect(self.create_requested)

        self.toolButton_delete.setIcon(QIcon(I('trash.png')))
        self.toolButton_delete.clicked.connect(self.delete_bookmark)

        self.toolButton_export.setIcon(QIcon(I('back.png')))
        self.toolButton_export.clicked.connect(self.export_bookmarks)

        self.toolButton_import.setIcon(QIcon(I('forward.png')))
        self.toolButton_import.clicked.connect(self.import_bookmarks)

    @pyqtSlot(int)
    def on_comboBoxSort_currentIndexChanged(self, index):
        self.sort_by_name() if index else self.sort_by_pos()

    def item_activated(self, item):
        bm = self.item_to_bm(item)
        self.activated.emit(bm)

    def set_bookmarks(self, bookmarks=()):
        self.bookmarks_list.clear()

        if not self.sorted and bookmarks:  # default sort by position
            self.sorted = True
            bookmarks = self.sort_by_pos(bookmarks)

        for bm in bookmarks:
            if bm['title'] != 'calibre_current_page_bookmark':
                i = QListWidgetItem(bm['title'])
                i.setData(Qt.UserRole, self.bm_to_item(bm))
                i.setFlags(i.flags() | Qt.ItemIsEditable)
                self.bookmarks_list.addItem(i)
        if self.bookmarks_list.count() > 0:
            self.bookmarks_list.setCurrentItem(self.bookmarks_list.item(0), QItemSelectionModel.ClearAndSelect)

    def set_current_bookmark(self, bm):
        for i, q in enumerate(self):
            if bm == q:
                l = self.bookmarks_list
                item = l.item(i)
                l.setCurrentItem(item, QItemSelectionModel.ClearAndSelect)
                l.scrollToItem(item)

    def __iter__(self):
        for i in xrange(self.bookmarks_list.count()):
            yield self.item_to_bm(self.bookmarks_list.item(i))

    def item_changed(self, item):
        self.bookmarks_list.blockSignals(True)
        title = unicode(item.data(Qt.DisplayRole))
        if not title:
            title = _('Unknown')
            item.setData(Qt.DisplayRole, title)
        bm = self.item_to_bm(item)
        bm['title'] = title
        item.setData(Qt.UserRole, self.bm_to_item(bm))
        self.bookmarks_list.blockSignals(False)
        self.edited.emit(self.get_bookmarks())

    def delete_bookmark(self):
        row = self.bookmarks_list.currentRow()
        if row > -1:
            self.bookmarks_list.takeItem(row)
            self.edited.emit(self.get_bookmarks())

    def edit_bookmark(self):
        item = self.bookmarks_list.currentItem()
        if item is not None:
            self.bookmarks_list.editItem(item)

    def sort_by_name(self):
        bm = self.get_bookmarks()
        bm.sort(key=lambda x: sort_key(x['title']))
        self.set_bookmarks(bm)
        self.edited.emit(bm)

    def sort_by_pos(self, bm=None):
        from calibre.ebooks.epub.cfi.parse import cfi_sort_key

        def pos_key(b):
            if b.get('type', None) == 'cfi':
                return b['spine'], cfi_sort_key(b['pos'])
            return (None, None)

        if bm is not None:
            bm.sort(key=pos_key)
            return bm

        bm = self.get_bookmarks()
        bm.sort(key=pos_key)
        self.set_bookmarks(bm)
        self.edited.emit(bm)

    def bm_to_item(self, bm):
        return bytearray(cPickle.dumps(bm, -1))

    def item_to_bm(self, item):
        return cPickle.loads(bytes(item.data(Qt.UserRole)))

    def get_bookmarks(self):
        return list(self)

    def export_bookmarks(self):
        filename = choose_save_file(
            self, 'export-viewer-bookmarks', _('Export Bookmarks'),
            filters=[(_('Saved Bookmarks'), ['pickle'])], all_files=False, initial_filename='bookmarks.pickle')
        if filename:
            with open(filename, 'wb') as fileobj:
                cPickle.dump(self.get_bookmarks(), fileobj, -1)

    def import_bookmarks(self):
        files = choose_files(self, 'export-viewer-bookmarks', _('Import Bookmarks'),
                             filters=[(_('Saved Bookmarks'), ['pickle'])], all_files=False,
                             select_only_single_file=True)
        if not files:
            return
        filename = files[0]

        imported = None
        with open(filename, 'rb') as fileobj:
            imported = cPickle.load(fileobj)

        if imported is not None:
            bad = False
            try:
                for bm in imported:
                    if 'title' not in bm:
                        bad = True
                        break
            except Exception:
                pass

            if not bad:
                bookmarks = self.get_bookmarks()
                for bm in imported:
                    if bm not in bookmarks:
                        bookmarks.append(bm)
                self.set_bookmarks([bm for bm in bookmarks if bm['title'] != 'calibre_current_page_bookmark'])
                self.edited.emit(self.get_bookmarks())
