# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/7597ECC22B316B49/programs/linux/calibre/src/calibre/gui2/viewer/qlistwidget/qlistwidgetBookmark.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        Form.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        Form.setStyleSheet("QListView::item { padding: 0.5ex }")
        Form.setDragEnabled(True)
        Form.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        Form.setDefaultDropAction(QtCore.Qt.MoveAction)
        Form.setAlternatingRowColors(True)
        self.ac_edit = QtWidgets.QAction(Form)
        self.ac_edit.setObjectName("ac_edit")
        self.ac_delete = QtWidgets.QAction(Form)
        self.ac_delete.setObjectName("ac_delete")
        self.ac_sort = QtWidgets.QAction(Form)
        self.ac_sort.setObjectName("ac_sort")
        self.ac_sort_pos = QtWidgets.QAction(Form)
        self.ac_sort_pos.setObjectName("ac_sort_pos")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        Form.setWindowTitle(_("Form"))
        self.ac_edit.setText(_("Edit"))
        self.ac_delete.setText(_("Delete"))
        self.ac_sort.setText(_("Name"))
        self.ac_sort_pos.setText(_("Position"))

