# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/7597ECC22B316B49/programs/linux/calibre/src/calibre/gui2/preferences/behavior.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(941, 563)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.opt_new_version_notification = QtWidgets.QCheckBox(Form)
        self.opt_new_version_notification.setObjectName("opt_new_version_notification")
        self.gridLayout.addWidget(self.opt_new_version_notification, 1, 0, 1, 1)
        self.opt_bools_are_tristate = QtWidgets.QCheckBox(Form)
        self.opt_bools_are_tristate.setObjectName("opt_bools_are_tristate")
        self.gridLayout.addWidget(self.opt_bools_are_tristate, 1, 1, 1, 1)
        self.opt_upload_news_to_device = QtWidgets.QCheckBox(Form)
        self.opt_upload_news_to_device.setObjectName("opt_upload_news_to_device")
        self.gridLayout.addWidget(self.opt_upload_news_to_device, 3, 0, 1, 1)
        self.opt_delete_news_from_library_on_upload = QtWidgets.QCheckBox(Form)
        self.opt_delete_news_from_library_on_upload.setObjectName("opt_delete_news_from_library_on_upload")
        self.gridLayout.addWidget(self.opt_delete_news_from_library_on_upload, 3, 1, 1, 1)
        self.hboxlayout = QtWidgets.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")
        self.label_23 = QtWidgets.QLabel(Form)
        self.label_23.setObjectName("label_23")
        self.hboxlayout.addWidget(self.label_23)
        self.opt_output_format = QtWidgets.QComboBox(Form)
        self.opt_output_format.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.opt_output_format.setMinimumContentsLength(10)
        self.opt_output_format.setObjectName("opt_output_format")
        self.hboxlayout.addWidget(self.opt_output_format)
        self.gridLayout.addLayout(self.hboxlayout, 5, 0, 1, 1)
        self.hboxlayout1 = QtWidgets.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.hboxlayout1.addWidget(self.label_2)
        self.opt_network_timeout = QtWidgets.QSpinBox(Form)
        self.opt_network_timeout.setMinimum(2)
        self.opt_network_timeout.setMaximum(120)
        self.opt_network_timeout.setProperty("value", 5)
        self.opt_network_timeout.setObjectName("opt_network_timeout")
        self.hboxlayout1.addWidget(self.opt_network_timeout)
        self.gridLayout.addLayout(self.hboxlayout1, 5, 1, 1, 1)
        self.hboxlayout2 = QtWidgets.QHBoxLayout()
        self.hboxlayout2.setObjectName("hboxlayout2")
        self.priority_label = QtWidgets.QLabel(Form)
        self.priority_label.setObjectName("priority_label")
        self.hboxlayout2.addWidget(self.priority_label)
        self.opt_worker_process_priority = QtWidgets.QComboBox(Form)
        self.opt_worker_process_priority.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.opt_worker_process_priority.setMinimumContentsLength(20)
        self.opt_worker_process_priority.setObjectName("opt_worker_process_priority")
        self.opt_worker_process_priority.addItem("")
        self.opt_worker_process_priority.addItem("")
        self.opt_worker_process_priority.addItem("")
        self.hboxlayout2.addWidget(self.opt_worker_process_priority)
        self.gridLayout.addLayout(self.hboxlayout2, 7, 0, 1, 1)
        self.hboxlayout3 = QtWidgets.QHBoxLayout()
        self.hboxlayout3.setObjectName("hboxlayout3")
        self.label_170 = QtWidgets.QLabel(Form)
        self.label_170.setObjectName("label_170")
        self.hboxlayout3.addWidget(self.label_170)
        self.opt_virtual_lib_on_startup = QtWidgets.QComboBox(Form)
        self.opt_virtual_lib_on_startup.setMaximumSize(QtCore.QSize(250, 16777215))
        self.opt_virtual_lib_on_startup.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.opt_virtual_lib_on_startup.setMinimumContentsLength(15)
        self.opt_virtual_lib_on_startup.setObjectName("opt_virtual_lib_on_startup")
        self.hboxlayout3.addWidget(self.opt_virtual_lib_on_startup)
        self.gridLayout.addLayout(self.hboxlayout3, 7, 1, 1, 1)
        self.hboxlayout4 = QtWidgets.QHBoxLayout()
        self.hboxlayout4.setObjectName("hboxlayout4")
        self.edit_metadata_single_label = QtWidgets.QLabel(Form)
        self.edit_metadata_single_label.setObjectName("edit_metadata_single_label")
        self.hboxlayout4.addWidget(self.edit_metadata_single_label)
        self.opt_edit_metadata_single_layout = QtWidgets.QComboBox(Form)
        self.opt_edit_metadata_single_layout.setObjectName("opt_edit_metadata_single_layout")
        self.hboxlayout4.addWidget(self.opt_edit_metadata_single_layout)
        self.gridLayout.addLayout(self.hboxlayout4, 8, 0, 1, 1)
        self.groupBox_5 = QtWidgets.QGroupBox(Form)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.opt_input_order = QtWidgets.QListWidget(self.groupBox_5)
        self.opt_input_order.setAlternatingRowColors(True)
        self.opt_input_order.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.opt_input_order.setObjectName("opt_input_order")
        self.horizontalLayout_10.addWidget(self.opt_input_order)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.input_up_button = QtWidgets.QToolButton(self.groupBox_5)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(I("arrow-up.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.input_up_button.setIcon(icon)
        self.input_up_button.setObjectName("input_up_button")
        self.verticalLayout_10.addWidget(self.input_up_button)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_10.addItem(spacerItem)
        self.input_down_button = QtWidgets.QToolButton(self.groupBox_5)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(I("arrow-down.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.input_down_button.setIcon(icon1)
        self.input_down_button.setObjectName("input_down_button")
        self.verticalLayout_10.addWidget(self.input_down_button)
        self.horizontalLayout_10.addLayout(self.verticalLayout_10)
        self.verticalLayout_11.addLayout(self.horizontalLayout_10)
        self.gridLayout.addWidget(self.groupBox_5, 19, 0, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.opt_internally_viewed_formats = QtWidgets.QListWidget(self.groupBox_3)
        self.opt_internally_viewed_formats.setAlternatingRowColors(True)
        self.opt_internally_viewed_formats.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.opt_internally_viewed_formats.setObjectName("opt_internally_viewed_formats")
        self.gridLayout_4.addWidget(self.opt_internally_viewed_formats, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_3, 19, 1, 1, 1)
        self.reset_confirmation_button = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reset_confirmation_button.sizePolicy().hasHeightForWidth())
        self.reset_confirmation_button.setSizePolicy(sizePolicy)
        self.reset_confirmation_button.setObjectName("reset_confirmation_button")
        self.gridLayout.addWidget(self.reset_confirmation_button, 8, 1, 1, 1)
        self.label_23.setBuddy(self.opt_output_format)
        self.label_2.setBuddy(self.opt_network_timeout)
        self.priority_label.setBuddy(self.opt_worker_process_priority)
        self.label_170.setBuddy(self.opt_virtual_lib_on_startup)
        self.edit_metadata_single_label.setBuddy(self.opt_edit_metadata_single_layout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        Form.setWindowTitle(_("Form"))
        self.opt_new_version_notification.setText(_("Show notification when &new version is available"))
        self.opt_bools_are_tristate.setToolTip(_("If checked, Yes/No custom columns values can be Yes, No, or Unknown.\n"
"If not checked, the values can be Yes or No."))
        self.opt_bools_are_tristate.setText(_("Yes/No columns have three values (Requires restart)"))
        self.opt_upload_news_to_device.setText(_("Automatically send downloaded &news to ebook reader"))
        self.opt_delete_news_from_library_on_upload.setText(_("&Delete news from library when it is automatically sent to reader"))
        self.label_23.setText(_("Preferred &output format:"))
        self.label_2.setText(_("Default network &timeout:"))
        self.opt_network_timeout.setToolTip(_("Set the default timeout for network fetches (i.e. anytime we go out to the internet to get information)"))
        self.opt_network_timeout.setSuffix(_(" seconds"))
        self.priority_label.setText(_("Job &priority:"))
        self.opt_worker_process_priority.setItemText(0, _("Normal"))
        self.opt_worker_process_priority.setItemText(1, _("High"))
        self.opt_worker_process_priority.setItemText(2, _("Low"))
        self.label_170.setText(_("Virtual library to apply when the current library is opened:"))
        self.opt_virtual_lib_on_startup.setToolTip(_("Use this virtual library on calibre startup if the current library is being used. Also applied when switching to this library. Note that this setting is per library. "))
        self.edit_metadata_single_label.setText(_("Edit metadata (single) layout:"))
        self.opt_edit_metadata_single_layout.setToolTip(_("Choose a different layout for the Edit Metadata dialog. The compact metadata layout favors editing custom metadata over changing covers and formats."))
        self.groupBox_5.setTitle(_("Preferred &input format order:"))
        self.input_up_button.setText(_("..."))
        self.input_down_button.setText(_("..."))
        self.groupBox_3.setTitle(_("Use internal &viewer for:"))
        self.reset_confirmation_button.setText(_("Reset all disabled &confirmation dialogs"))


