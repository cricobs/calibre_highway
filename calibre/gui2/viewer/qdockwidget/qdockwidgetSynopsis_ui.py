# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/7597ECC22B316B49/programs/linux/calibre/src/calibre/gui2/viewer/qdockwidget/qdockwidgetSynopsis.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName("DockWidget")
        DockWidget.resize(94, 59)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.qstackedwidgetSynopsis = QstackedwidgetSynopsis(self.dockWidgetContents)
        self.qstackedwidgetSynopsis.setObjectName("qstackedwidgetSynopsis")
        self.verticalLayout_3.addWidget(self.qstackedwidgetSynopsis)
        DockWidget.setWidget(self.dockWidgetContents)
        self.qactionSave = QtWidgets.QAction(DockWidget)
        self.qactionSave.setObjectName("qactionSave")
        self.qactionPreview = QtWidgets.QAction(DockWidget)
        self.qactionPreview.setObjectName("qactionPreview")

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):

        DockWidget.setWindowTitle(_("Synopsis"))
        self.qactionSave.setText(_("Save"))
        self.qactionPreview.setText(_("Preview"))

from calibre.gui2.viewer.qstackedwidget.qstackedwidgetSynopsis import QstackedwidgetSynopsis
