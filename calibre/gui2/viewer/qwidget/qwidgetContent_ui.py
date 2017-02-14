# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/7597ECC22B316B49/programs/linux/calibre/src/calibre/gui2/viewer/qwidget/qwidgetContent.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(133, 47)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.search = QcomboboxSearch(Form)
        self.search.setMinimumContentsLength(15)
        self.search.setObjectName("search")
        self.horizontalLayout.addWidget(self.search)
        self.toolButton = QtWidgets.QToolButton(Form)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout.addWidget(self.toolButton)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        Form.setWindowTitle(_("Form"))
        self.search.setToolTip(_("\'Search for text in the Table of Contents\'"))
        self.toolButton.setToolTip(_("Find next match"))
        self.toolButton.setText(_("..."))

from calibre.gui2.viewer.qcombobox.qcomboboxSearch import QcomboboxSearch
