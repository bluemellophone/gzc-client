# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GPSForm.ui'
#
# Created: Sat Feb 21 13:58:44 2015
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_GPSForm(object):
    def setupUi(self, GPSForm):
        GPSForm.setObjectName(_fromUtf8("GPSForm"))
        GPSForm.resize(320, 237)
        font = QtGui.QFont()
        font.setPointSize(12)
        GPSForm.setFont(font)
        self.verticalLayout = QtGui.QVBoxLayout(GPSForm)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.layout = QtGui.QVBoxLayout()
        self.layout.setSpacing(15)
        self.layout.setObjectName(_fromUtf8("layout"))
        self.id_layout = QtGui.QGroupBox(GPSForm)
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
        self.color_input_space = QtGui.QVBoxLayout()
        self.color_input_space.setObjectName(_fromUtf8("color_input_space"))
        self.formLayout_4.setLayout(0, QtGui.QFormLayout.FieldRole, self.color_input_space)
        self.layout.addWidget(self.id_layout)
        self.sync_layout = QtGui.QGroupBox(GPSForm)
        self.sync_layout.setObjectName(_fromUtf8("sync_layout"))
        self.formLayout_6 = QtGui.QFormLayout(self.sync_layout)
        self.formLayout_6.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_6.setObjectName(_fromUtf8("formLayout_6"))
        self.time_label = QtGui.QLabel(self.sync_layout)
        self.time_label.setObjectName(_fromUtf8("time_label"))
        self.formLayout_6.setWidget(0, QtGui.QFormLayout.LabelRole, self.time_label)
        self.time_input = QtGui.QTimeEdit(self.sync_layout)
        self.time_input.setMinimumSize(QtCore.QSize(0, 0))
        self.time_input.setObjectName(_fromUtf8("time_input"))
        self.formLayout_6.setWidget(0, QtGui.QFormLayout.FieldRole, self.time_input)
        self.sync_status = QtGui.QLabel(self.sync_layout)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.sync_status.setFont(font)
        self.sync_status.setStyleSheet(_fromUtf8("color: #666;"))
        self.sync_status.setText(_fromUtf8(""))
        self.sync_status.setObjectName(_fromUtf8("sync_status"))
        self.formLayout_6.setWidget(1, QtGui.QFormLayout.SpanningRole, self.sync_status)
        self.layout.addWidget(self.sync_layout)
        self.verticalLayout.addLayout(self.layout)

        self.retranslateUi(GPSForm)
        QtCore.QMetaObject.connectSlotsByName(GPSForm)

    def retranslateUi(self, GPSForm):
        GPSForm.setWindowTitle(_translate("GPSForm", "Form", None))
        self.id_layout.setTitle(_translate("GPSForm", "1 - Input Identification Information:", None))
        self.color_label.setText(_translate("GPSForm", "Car Color", None))
        self.numer_label.setText(_translate("GPSForm", "Car #", None))
        self.sync_layout.setTitle(_translate("GPSForm", "2 - Synchronize GPS Information:", None))
        self.time_label.setText(_translate("GPSForm", "Car Start Time", None))
        self.time_input.setDisplayFormat(_translate("GPSForm", "HH:mm", None))

