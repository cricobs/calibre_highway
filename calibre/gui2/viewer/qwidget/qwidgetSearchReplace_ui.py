# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/7597ECC22B316B49/programs/linux/calibre/src/calibre/gui2/viewer/qwidget/qwidgetSearchReplace.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(212, 47)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.qcomboboxSearch = QcomboboxSearchReplace(Form)
        self.qcomboboxSearch.setObjectName("qcomboboxSearch")
        self.horizontalLayout.addWidget(self.qcomboboxSearch)
        self.qcomboboxReplace = QcomboboxSearchReplace(Form)
        self.qcomboboxReplace.setObjectName("qcomboboxReplace")
        self.horizontalLayout.addWidget(self.qcomboboxReplace)
        self.qwidgetUpDown = QwidgetUpDown(Form)
        self.qwidgetUpDown.setStyleSheet("background-color: rgba(0,0,0,0)")
        self.qwidgetUpDown.setObjectName("qwidgetUpDown")
        self.horizontalLayout.addWidget(self.qwidgetUpDown)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        Form.setWindowTitle(_("Form"))

from calibre.gui2.viewer.qcombobox.qcomboboxSearchReplace import QcomboboxSearchReplace
from calibre.gui2.viewer.qwidget.qwidgetUpDown import QwidgetUpDown
