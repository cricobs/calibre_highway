# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/7597ECC22B316B49/programs/linux/calibre/src/calibre/gui2/viewer/qdockwidget/qdockwidgetQwebinspector.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName("DockWidget")
        DockWidget.resize(400, 367)
        DockWidget.setMinimumSize(QtCore.QSize(73, 333))
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setContentsMargins(0, -1, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.qstackedwidget = Qstackedwidget(self.dockWidgetContents)
        self.qstackedwidget.setObjectName("qstackedwidget")
        self.verticalLayout.addWidget(self.qstackedwidget)
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):

        DockWidget.setWindowTitle(_("DockWidget"))

from calibre.gui2.viewer.qstackedwidget.qstackedwidget import Qstackedwidget
