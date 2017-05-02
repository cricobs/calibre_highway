# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/7597ECC22B316B49/programs/linux/calibre/src/calibre/gui2/viewer/qwidget/qwidgetUpDown.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(94, 60)
        Form.setStyleSheet("")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.qtoolbuttonUp = QtWidgets.QToolButton(Form)
        self.qtoolbuttonUp.setMaximumSize(QtCore.QSize(18, 16777215))
        self.qtoolbuttonUp.setStyleSheet(" QToolButton {\n"
"     border:0;\n"
"    margin: 0;\n"
"    border-radius: 2px;\n"
" }\n"
"\n"
"QToolButton:hover\n"
"{\n"
"     border: 1px solid rgb(237, 237, 237);\n"
"}\n"
"\n"
"QToolButton:pressed\n"
"{\n"
"     border: 2px solid rgb(237, 237, 237);\n"
"}")
        self.qtoolbuttonUp.setObjectName("qtoolbuttonUp")
        self.verticalLayout.addWidget(self.qtoolbuttonUp)
        self.qtoolbuttonDown = QtWidgets.QToolButton(Form)
        self.qtoolbuttonDown.setMaximumSize(QtCore.QSize(18, 16777215))
        self.qtoolbuttonDown.setStyleSheet(" QToolButton {\n"
"     border:0;\n"
"    margin: 0;\n"
"    border-radius: 2px;\n"
" }\n"
"\n"
"QToolButton:hover\n"
"{\n"
"     border: 1px solid rgb(237, 237, 237);\n"
"}\n"
"\n"
"QToolButton:pressed\n"
"{\n"
"     border: 2px solid rgb(237, 237, 237);\n"
"}")
        self.qtoolbuttonDown.setObjectName("qtoolbuttonDown")
        self.verticalLayout.addWidget(self.qtoolbuttonDown)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        Form.setWindowTitle(_("Form"))
        self.qtoolbuttonUp.setText(_("..."))
        self.qtoolbuttonDown.setText(_("..."))

