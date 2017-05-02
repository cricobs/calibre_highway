# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/7597ECC22B316B49/programs/linux/calibre/src/calibre/gui2/viewer/qwidget/qwidgetFootnote.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(361, 130)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.view = QwebviewFootnote(Form)
        self.view.setProperty("url", QtCore.QUrl("about:blank"))
        self.view.setObjectName("view")
        self.gridLayout.addWidget(self.view, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        Form.setWindowTitle(_("Form"))

from calibre.gui2.viewer.qwebview.qwebviewFootnote import QwebviewFootnote
