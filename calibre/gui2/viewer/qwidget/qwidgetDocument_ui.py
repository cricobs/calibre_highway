# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/7597ECC22B316B49/programs/linux/calibre/src/calibre/gui2/viewer/qwidget/qwidgetDocument.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_centralwidget(object):
    def setupUi(self, centralwidget):
        centralwidget.setObjectName("centralwidget")
        centralwidget.resize(819, 635)
        self.gridLayout = QtWidgets.QGridLayout(centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontal_scrollbar = QtWidgets.QScrollBar(centralwidget)
        self.horizontal_scrollbar.setOrientation(QtCore.Qt.Horizontal)
        self.horizontal_scrollbar.setObjectName("horizontal_scrollbar")
        self.gridLayout.addWidget(self.horizontal_scrollbar, 1, 0, 1, 1)
        self.vertical_scrollbar = QtWidgets.QScrollBar(centralwidget)
        self.vertical_scrollbar.setOrientation(QtCore.Qt.Vertical)
        self.vertical_scrollbar.setObjectName("vertical_scrollbar")
        self.gridLayout.addWidget(self.vertical_scrollbar, 0, 1, 1, 1)
        self.view = QwebviewDocument(centralwidget)
        self.view.setMinimumSize(QtCore.QSize(100, 100))
        self.view.setUrl(QtCore.QUrl("about:blank"))
        self.view.setObjectName("view")
        self.gridLayout.addWidget(self.view, 0, 0, 1, 1)

        self.retranslateUi(centralwidget)
        QtCore.QMetaObject.connectSlotsByName(centralwidget)

    def retranslateUi(self, centralwidget):
        pass

from calibre.gui2.viewer.qwebview.qwebviewDocument import QwebviewDocument
