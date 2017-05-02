# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/7597ECC22B316B49/programs/linux/calibre/src/calibre/gui2/viewer/qtreeview/qtreeviewContent.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(256, 192)
        Form.setMinimumSize(QtCore.QSize(80, 0))
        Form.setMouseTracking(True)
        Form.setFocusPolicy(QtCore.Qt.StrongFocus)
        Form.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        Form.setStyleSheet("                QTreeView {\n"
"                    background-color: palette(window);\n"
"                    color: palette(window-text);\n"
"                    border: none;\n"
"                }\n"
"\n"
"                QTreeView::item {\n"
"                    border: 1px solid transparent;\n"
"                    padding-top:0.5ex;\n"
"                    padding-bottom:0.5ex;\n"
"                }\n"
"\n"
"                QTreeView::item:hover {\n"
"                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e7effd, stop: 1 #cbdaf1);\n"
"                    border: 1px solid #bfcde4;\n"
"                    border-radius: 6px;\n"
"                }")
        Form.setHeaderHidden(True)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        Form.setWindowTitle(_("Form"))

