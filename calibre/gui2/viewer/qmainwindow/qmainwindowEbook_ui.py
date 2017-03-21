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
        QmainwindowEbook.resize(108, 118)
        self.qwidgetDocument = QwidgetDocument(QmainwindowEbook)
        self.qwidgetDocument.setObjectName("qwidgetDocument")
        self.qtoolbarEdit = QtoolbarEdit(QmainwindowEbook)
        self.qtoolbarEdit.setIconSize(QtCore.QSize(18, 18))
        self.qtoolbarEdit.setObjectName("qtoolbarEdit")
        QmainwindowEbook.addToolBar(QtCore.Qt.LeftToolBarArea, self.qtoolbarEdit)
        self.qdockwidgetContent = QdockwidgetContent(QmainwindowEbook)
        self.qdockwidgetContent.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.qdockwidgetContent.setObjectName("qdockwidgetContent")
        QmainwindowEbook.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.qdockwidgetContent)
        self.qdockwidgetBookmark = QdockwidgetBookmark(QmainwindowEbook)
        self.qdockwidgetBookmark.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.qdockwidgetBookmark.setObjectName("qdockwidgetBookmark")
        QmainwindowEbook.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.qdockwidgetBookmark)
        self.qdockwidgetFootnote = QdockwidgetFootnote(QmainwindowEbook)
        self.qdockwidgetFootnote.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.qdockwidgetFootnote.setObjectName("qdockwidgetFootnote")
        QmainwindowEbook.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.qdockwidgetFootnote)
        self.qdockwidgetSynopsis = QdockwidgetSynopsis(QmainwindowEbook)
        self.qdockwidgetSynopsis.setObjectName("qdockwidgetSynopsis")
        QmainwindowEbook.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.qdockwidgetSynopsis)

        self.retranslateUi(QmainwindowEbook)
        QtCore.QMetaObject.connectSlotsByName(QmainwindowEbook)

    def retranslateUi(self, QmainwindowEbook):

        QmainwindowEbook.setWindowTitle(_("E-book viewer"))
        self.qtoolbarEdit.setWindowTitle(_("toolBar"))
        self.qdockwidgetContent.setWindowTitle(_("Table of Contents"))
        self.qdockwidgetBookmark.setWindowTitle(_("Bookmark"))
        self.qdockwidgetFootnote.setWindowTitle(_("Footnotes"))
        self.qdockwidgetSynopsis.setWindowTitle(_("Synopsis"))

from calibre.gui2.viewer.qdockwidget.qdockwidgetBookmark import QdockwidgetBookmark
from calibre.gui2.viewer.qdockwidget.qdockwidgetContent import QdockwidgetContent
from calibre.gui2.viewer.qdockwidget.qdockwidgetFootnote import QdockwidgetFootnote
from calibre.gui2.viewer.qdockwidget.qdockwidgetSynopsis import QdockwidgetSynopsis
from calibre.gui2.viewer.qtoolbar.qtoolbarEdit import QtoolbarEdit
from calibre.gui2.viewer.qwidget.qwidgetDocument import QwidgetDocument
