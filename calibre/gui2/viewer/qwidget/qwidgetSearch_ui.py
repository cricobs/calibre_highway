# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/7597ECC22B316B49/programs/linux/calibre/src/calibre/gui2/viewer/qwidget/qwidgetSearch.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(343, 42)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.reference = QLineeditReference(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reference.sizePolicy().hasHeightForWidth())
        self.reference.setSizePolicy(sizePolicy)
        self.reference.setObjectName("reference")
        self.horizontalLayout.addWidget(self.reference)
        self.pos = QdoublespinboxPosition(Form)
        self.pos.setObjectName("pos")
        self.horizontalLayout.addWidget(self.pos)
        self.search = QcomboboxSearch(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search.sizePolicy().hasHeightForWidth())
        self.search.setSizePolicy(sizePolicy)
        self.search.setObjectName("search")
        self.horizontalLayout.addWidget(self.search)
        self.horizontalLayoutToolButtons = QtWidgets.QHBoxLayout()
        self.horizontalLayoutToolButtons.setSpacing(1)
        self.horizontalLayoutToolButtons.setObjectName("horizontalLayoutToolButtons")
        self.horizontalLayout.addLayout(self.horizontalLayoutToolButtons)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        Form.setWindowTitle(_("Form"))

from calibre.gui2.viewer.qcombobox.qcomboboxSearch import QcomboboxSearch
from calibre.gui2.viewer.qdoublespinbox.qdoublespinboxPosition import QdoublespinboxPosition
from calibre.gui2.viewer.qlineedit.qlineeditReference import QLineeditReference
