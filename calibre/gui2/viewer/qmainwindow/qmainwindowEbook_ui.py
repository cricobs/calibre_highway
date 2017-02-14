# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/7597ECC22B316B49/programs/linux/calibre/src/calibre/gui2/viewer/qmainwindow/qmainwindowEbook.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_QmainwindowEbook(object):
    def setupUi(self, QmainwindowEbook):
        QmainwindowEbook.setObjectName("QmainwindowEbook")
        QmainwindowEbook.resize(1081, 648)
        self.centralwidget = QtWidgets.QWidget(QmainwindowEbook)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.vertical_scrollbar = QtWidgets.QScrollBar(self.centralwidget)
        self.vertical_scrollbar.setOrientation(QtCore.Qt.Vertical)
        self.vertical_scrollbar.setObjectName("vertical_scrollbar")
        self.gridLayout.addWidget(self.vertical_scrollbar, 1, 1, 1, 1)
        self.horizontal_scrollbar = QtWidgets.QScrollBar(self.centralwidget)
        self.horizontal_scrollbar.setOrientation(QtCore.Qt.Horizontal)
        self.horizontal_scrollbar.setObjectName("horizontal_scrollbar")
        self.gridLayout.addWidget(self.horizontal_scrollbar, 2, 0, 1, 1)
        self.view = QwebviewDocument(self.centralwidget)
        self.view.setMinimumSize(QtCore.QSize(100, 100))
        self.view.setUrl(QtCore.QUrl("about:blank"))
        self.view.setObjectName("view")
        self.gridLayout.addWidget(self.view, 1, 0, 1, 1)
        self.qwidgetSearch = QwidgetSearch(self.centralwidget)
        self.qwidgetSearch.setObjectName("qwidgetSearch")
        self.gridLayout.addWidget(self.qwidgetSearch, 0, 0, 1, 1)
        QmainwindowEbook.setCentralWidget(self.centralwidget)
        self.tool_bar = QtoolbarEdit(QmainwindowEbook)
        self.tool_bar.setIconSize(QtCore.QSize(18, 18))
        self.tool_bar.setObjectName("tool_bar")
        QmainwindowEbook.addToolBar(QtCore.Qt.TopToolBarArea, self.tool_bar)
        self.toc_dock = Qdockwidget(QmainwindowEbook)
        self.toc_dock.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.toc_dock.setObjectName("toc_dock")
        self.toc_container = QtWidgets.QWidget()
        self.toc_container.setObjectName("toc_container")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.toc_container)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.toc_search = QwidgetContent(self.toc_container)
        self.toc_search.setObjectName("toc_search")
        self.verticalLayout.addWidget(self.toc_search)
        self.toc = QtreeviewContent(self.toc_container)
        self.toc.setObjectName("toc")
        self.verticalLayout.addWidget(self.toc)
        self.toc_dock.setWidget(self.toc_container)
        QmainwindowEbook.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.toc_dock)
        self.bookmarks_dock = Qdockwidget(QmainwindowEbook)
        self.bookmarks_dock.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.bookmarks_dock.setObjectName("bookmarks_dock")
        self.bookmarks = QwidgetBookmark()
        self.bookmarks.setObjectName("bookmarks")
        self.bookmarks_dock.setWidget(self.bookmarks)
        QmainwindowEbook.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.bookmarks_dock)
        self.footnotes_dock = Qdockwidget(QmainwindowEbook)
        self.footnotes_dock.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.footnotes_dock.setObjectName("footnotes_dock")
        self.footnotes_view = QwidgetFootnote()
        self.footnotes_view.setObjectName("footnotes_view")
        self.footnotes_dock.setWidget(self.footnotes_view)
        QmainwindowEbook.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.footnotes_dock)
        self.qdockwidgetSynopsis = QdockwidgetSynopsis(QmainwindowEbook)
        self.qdockwidgetSynopsis.setObjectName("qdockwidgetSynopsis")
        QmainwindowEbook.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.qdockwidgetSynopsis)

        self.retranslateUi(QmainwindowEbook)
        QtCore.QMetaObject.connectSlotsByName(QmainwindowEbook)

    def retranslateUi(self, QmainwindowEbook):

        QmainwindowEbook.setWindowTitle(_("E-book viewer"))
        self.tool_bar.setWindowTitle(_("toolBar"))
        self.toc_dock.setWindowTitle(_("Table of Contents"))
        self.bookmarks_dock.setWindowTitle(_("Bookmarks"))
        self.footnotes_dock.setWindowTitle(_("Footnotes"))
        self.qdockwidgetSynopsis.setWindowTitle(_("Synopsis"))

from calibre.gui2.viewer.qdockwidget.qdockwidget import Qdockwidget
from calibre.gui2.viewer.qdockwidget.qdockwidgetSynopsis import QdockwidgetSynopsis
from calibre.gui2.viewer.qtoolbar.qtoolbarEdit import QtoolbarEdit
from calibre.gui2.viewer.qtreeview.qtreeviewContent import QtreeviewContent
from calibre.gui2.viewer.qwebview.qwebviewDocument import QwebviewDocument
from calibre.gui2.viewer.qwidget.qwidgetBookmark import QwidgetBookmark
from calibre.gui2.viewer.qwidget.qwidgetContent import QwidgetContent
from calibre.gui2.viewer.qwidget.qwidgetFootnote import QwidgetFootnote
from calibre.gui2.viewer.qwidget.qwidgetSearch import QwidgetSearch
