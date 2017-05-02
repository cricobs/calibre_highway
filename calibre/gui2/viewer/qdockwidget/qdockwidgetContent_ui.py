# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/7597ECC22B316B49/programs/linux/calibre/src/calibre/gui2/viewer/qdockwidget/qdockwidgetContent.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_toc_dock(object):
    def setupUi(self, toc_dock):
        toc_dock.setObjectName("toc_dock")
        toc_dock.resize(256, 233)
        toc_dock.setFocusPolicy(QtCore.Qt.StrongFocus)
        toc_dock.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.toc_container = QtWidgets.QWidget()
        self.toc_container.setObjectName("toc_container")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.toc_container)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.qtreeviewContent = QtreeviewContent(self.toc_container)
        self.qtreeviewContent.setObjectName("qtreeviewContent")
        self.verticalLayout.addWidget(self.qtreeviewContent)
        toc_dock.setWidget(self.toc_container)

        self.retranslateUi(toc_dock)
        QtCore.QMetaObject.connectSlotsByName(toc_dock)

    def retranslateUi(self, toc_dock):

        toc_dock.setWindowTitle(_("Table of Contents"))

from calibre.gui2.viewer.qtreeview.qtreeviewContent import QtreeviewContent
