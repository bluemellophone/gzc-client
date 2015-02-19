# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ImageForm.ui'
#
# Created: Thu Feb 19 13:34:34 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ImageForm(object):
    def setupUi(self, ImageForm):
        ImageForm.setObjectName(_fromUtf8("ImageForm"))
        ImageForm.resize(366, 426)
        ImageForm.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        ImageForm.setFont(font)
        ImageForm.setStyleSheet(_fromUtf8(""))
        self.horizontalLayout = QtGui.QHBoxLayout(ImageForm)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.layout = QtGui.QVBoxLayout()
        self.layout.setSpacing(15)
        self.layout.setObjectName(_fromUtf8("layout"))
        self.drive_layout = QtGui.QGroupBox(ImageForm)
        self.drive_layout.setSizeIncrement(QtCore.QSize(1, 1))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.drive_layout.setFont(font)
        self.drive_layout.setObjectName(_fromUtf8("drive_layout"))
        self.formLayout = QtGui.QFormLayout(self.drive_layout)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.drive_browse = QtGui.QPushButton(self.drive_layout)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.drive_browse.sizePolicy().hasHeightForWidth())
        self.drive_browse.setSizePolicy(sizePolicy)
        self.drive_browse.setMinimumSize(QtCore.QSize(0, 0))
        self.drive_browse.setObjectName(_fromUtf8("drive_browse"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.SpanningRole, self.drive_browse)
        self.drive_display = QtGui.QLineEdit(self.drive_layout)
        self.drive_display.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.drive_display.setFont(font)
        self.drive_display.setObjectName(_fromUtf8("drive_display"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.SpanningRole, self.drive_display)
        self.layout.addWidget(self.drive_layout)
        self.id_layout = QtGui.QGroupBox(ImageForm)
        self.id_layout.setObjectName(_fromUtf8("id_layout"))
        self.formLayout_4 = QtGui.QFormLayout(self.id_layout)
        self.formLayout_4.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_4.setObjectName(_fromUtf8("formLayout_4"))
        self.color_label = QtGui.QLabel(self.id_layout)
        self.color_label.setObjectName(_fromUtf8("color_label"))
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.LabelRole, self.color_label)
        self.numer_label = QtGui.QLabel(self.id_layout)
        self.numer_label.setObjectName(_fromUtf8("numer_label"))
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.LabelRole, self.numer_label)
        self.number_input = QtGui.QSpinBox(self.id_layout)
        self.number_input.setMinimumSize(QtCore.QSize(0, 0))
        self.number_input.setObjectName(_fromUtf8("number_input"))
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.FieldRole, self.number_input)
        self.id_label = QtGui.QLabel(self.id_layout)
        self.id_label.setObjectName(_fromUtf8("id_label"))
        self.formLayout_4.setWidget(2, QtGui.QFormLayout.LabelRole, self.id_label)
        self.letter_input = QtGui.QComboBox(self.id_layout)
        self.letter_input.setMinimumSize(QtCore.QSize(0, 0))
        self.letter_input.setObjectName(_fromUtf8("letter_input"))
        self.formLayout_4.setWidget(2, QtGui.QFormLayout.FieldRole, self.letter_input)
        self.color_input_space = QtGui.QVBoxLayout()
        self.color_input_space.setObjectName(_fromUtf8("color_input_space"))
        self.formLayout_4.setLayout(0, QtGui.QFormLayout.FieldRole, self.color_input_space)
        self.layout.addWidget(self.id_layout)
        self.sync_layout = QtGui.QGroupBox(ImageForm)
        self.sync_layout.setObjectName(_fromUtf8("sync_layout"))
        self.formLayout_6 = QtGui.QFormLayout(self.sync_layout)
        self.formLayout_6.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_6.setObjectName(_fromUtf8("formLayout_6"))
        self.name_label = QtGui.QLabel(self.sync_layout)
        self.name_label.setObjectName(_fromUtf8("name_label"))
        self.formLayout_6.setWidget(0, QtGui.QFormLayout.LabelRole, self.name_label)
        self.name_input = QtGui.QLineEdit(self.sync_layout)
        self.name_input.setMinimumSize(QtCore.QSize(0, 0))
        self.name_input.setObjectName(_fromUtf8("name_input"))
        self.formLayout_6.setWidget(0, QtGui.QFormLayout.FieldRole, self.name_input)
        self.time_label = QtGui.QLabel(self.sync_layout)
        self.time_label.setObjectName(_fromUtf8("time_label"))
        self.formLayout_6.setWidget(2, QtGui.QFormLayout.LabelRole, self.time_label)
        self.time_input = QtGui.QTimeEdit(self.sync_layout)
        self.time_input.setMinimumSize(QtCore.QSize(0, 0))
        self.time_input.setObjectName(_fromUtf8("time_input"))
        self.formLayout_6.setWidget(2, QtGui.QFormLayout.FieldRole, self.time_input)
        self.sync_status = QtGui.QLabel(self.sync_layout)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.sync_status.setFont(font)
        self.sync_status.setStyleSheet(_fromUtf8("color: #666;"))
        self.sync_status.setText(_fromUtf8(""))
        self.sync_status.setObjectName(_fromUtf8("sync_status"))
        self.formLayout_6.setWidget(1, QtGui.QFormLayout.SpanningRole, self.sync_status)
        self.layout.addWidget(self.sync_layout)
        self.horizontalLayout.addLayout(self.layout)

        self.retranslateUi(ImageForm)
        QtCore.QMetaObject.connectSlotsByName(ImageForm)

    def retranslateUi(self, ImageForm):
        ImageForm.setWindowTitle(_translate("ImageForm", "Form", None))
        self.drive_layout.setTitle(_translate("ImageForm", "1 - Select Drive With SD Card:", None))
        self.drive_browse.setText(_translate("ImageForm", "Browse", None))
        self.id_layout.setTitle(_translate("ImageForm", "2 - Input Identification Information:", None))
        self.color_label.setText(_translate("ImageForm", "Car Color", None))
        self.numer_label.setText(_translate("ImageForm", "Car #", None))
        self.id_label.setText(_translate("ImageForm", "ID Letter", None))
        self.sync_layout.setTitle(_translate("ImageForm", "3 - Synchronize Image Information:", None))
        self.name_label.setText(_translate("ImageForm", "First Image Name", None))
        self.time_label.setText(_translate("ImageForm", "First Image Time", None))
        self.time_input.setDisplayFormat(_translate("ImageForm", "HH:mm", None))

