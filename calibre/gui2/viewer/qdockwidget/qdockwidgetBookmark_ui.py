# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/7597ECC22B316B49/programs/linux/calibre/src/calibre/gui2/viewer/qdockwidget/qdockwidgetBookmark.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName("DockWidget")
        DockWidget.resize(400, 300)
        self.qwidgetBookmark = QwidgetBookmark()
        self.qwidgetBookmark.setObjectName("qwidgetBookmark")
        DockWidget.setWidget(self.qwidgetBookmark)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):

        DockWidget.setWindowTitle(_("DockWidget"))

from calibre.gui2.viewer.qwidget.qwidgetBookmark import QwidgetBookmark
