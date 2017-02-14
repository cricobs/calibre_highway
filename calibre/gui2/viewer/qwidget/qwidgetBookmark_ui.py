# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/7597ECC22B316B49/programs/linux/calibre/src/calibre/gui2/viewer/qwidget/qwidgetBookmark.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(426, 300)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.bookmarks_list = QlistwidgetBookmark(Form)
        self.bookmarks_list.setObjectName("bookmarks_list")
        self.gridLayout.addWidget(self.bookmarks_list, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.toolButton_new = QtWidgets.QToolButton(Form)
        self.toolButton_new.setObjectName("toolButton_new")
        self.horizontalLayout.addWidget(self.toolButton_new)
        self.toolButton_delete = QtWidgets.QToolButton(Form)
        self.toolButton_delete.setObjectName("toolButton_delete")
        self.horizontalLayout.addWidget(self.toolButton_delete)
        self.toolButton_export = QtWidgets.QToolButton(Form)
        self.toolButton_export.setObjectName("toolButton_export")
        self.horizontalLayout.addWidget(self.toolButton_export)
        self.toolButton_import = QtWidgets.QToolButton(Form)
        self.toolButton_import.setObjectName("toolButton_import")
        self.horizontalLayout.addWidget(self.toolButton_import)
        self.comboBoxSort = QtWidgets.QComboBox(Form)
        self.comboBoxSort.setObjectName("comboBoxSort")
        self.comboBoxSort.addItem("")
        self.comboBoxSort.addItem("")
        self.horizontalLayout.addWidget(self.comboBoxSort)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        Form.setWindowTitle(_("Form"))
        self.toolButton_new.setToolTip(_("Create a new bookmark at the current location"))
        self.toolButton_new.setText(_("&New"))
        self.toolButton_delete.setToolTip(_("Remove the currently selected bookmark"))
        self.toolButton_delete.setText(_("&Delete"))
        self.toolButton_export.setToolTip(_("Export bookmarks"))
        self.toolButton_export.setText(_("&Export"))
        self.toolButton_import.setToolTip(_("Import bookmarks"))
        self.toolButton_import.setText(_("&Import"))
        self.comboBoxSort.setToolTip(_("Sort bookmarks by position or name"))
        self.comboBoxSort.setItemText(0, _("position"))
        self.comboBoxSort.setItemText(1, _("name"))

from calibre.gui2.viewer.qlistwidget.qlistwidgetBookmark import QlistwidgetBookmark
