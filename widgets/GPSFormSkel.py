# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GPSForm.ui'
#
# Created: Sun Feb 22 14:15:02 2015
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
        GPSForm.resize(458, 494)
        font = QtGui.QFont()
        font.setPointSize(12)
        GPSForm.setFont(font)
        self.verticalLayout = QtGui.QVBoxLayout(GPSForm)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.layout = QtGui.QVBoxLayout()
        self.layout.setSpacing(15)
        self.layout.setObjectName(_fromUtf8("layout"))
        self.id_layout = QtGui.QGroupBox(GPSForm)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.id_layout.setFont(font)
        self.id_layout.setStyleSheet(_fromUtf8("font-size:20px;color:#333;"))
        self.id_layout.setFlat(False)
        self.id_layout.setObjectName(_fromUtf8("id_layout"))
        self.formLayout_4 = QtGui.QFormLayout(self.id_layout)
        self.formLayout_4.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_4.setObjectName(_fromUtf8("formLayout_4"))
        self.color_input_space = QtGui.QVBoxLayout()
        self.color_input_space.setObjectName(_fromUtf8("color_input_space"))
        self.formLayout_4.setLayout(0, QtGui.QFormLayout.FieldRole, self.color_input_space)
        self.numer_label = QtGui.QLabel(self.id_layout)
        self.numer_label.setMinimumSize(QtCore.QSize(159, 0))
        self.numer_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.numer_label.setObjectName(_fromUtf8("numer_label"))
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.LabelRole, self.numer_label)
        self.color_label = QtGui.QLabel(self.id_layout)
        self.color_label.setMinimumSize(QtCore.QSize(159, 0))
        self.color_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.color_label.setObjectName(_fromUtf8("color_label"))
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.LabelRole, self.color_label)
        self.number_input = QtGui.QComboBox(self.id_layout)
        self.number_input.setMinimumSize(QtCore.QSize(0, 30))
        self.number_input.setObjectName(_fromUtf8("number_input"))
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.FieldRole, self.number_input)
        self.layout.addWidget(self.id_layout)
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        self.layout.addItem(spacerItem)
        self.sync_layout = QtGui.QGroupBox(GPSForm)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.sync_layout.setFont(font)
        self.sync_layout.setStyleSheet(_fromUtf8("font-size:20px;color:#333;"))
        self.sync_layout.setFlat(False)
        self.sync_layout.setObjectName(_fromUtf8("sync_layout"))
        self.formLayout_6 = QtGui.QFormLayout(self.sync_layout)
        self.formLayout_6.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_6.setObjectName(_fromUtf8("formLayout_6"))
        self.time_label = QtGui.QLabel(self.sync_layout)
        self.time_label.setMinimumSize(QtCore.QSize(159, 0))
        self.time_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.time_label.setObjectName(_fromUtf8("time_label"))
        self.formLayout_6.setWidget(0, QtGui.QFormLayout.LabelRole, self.time_label)
        self.time_input = QtGui.QTimeEdit(self.sync_layout)
        self.time_input.setMinimumSize(QtCore.QSize(0, 30))
        self.time_input.setAlignment(QtCore.Qt.AlignCenter)
        self.time_input.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.time_input.setObjectName(_fromUtf8("time_input"))
        self.formLayout_6.setWidget(0, QtGui.QFormLayout.FieldRole, self.time_input)
        self.layout.addWidget(self.sync_layout)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.layout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.layout)

        self.retranslateUi(GPSForm)
        QtCore.QMetaObject.connectSlotsByName(GPSForm)

    def retranslateUi(self, GPSForm):
        GPSForm.setWindowTitle(_translate("GPSForm", "Form", None))
        self.id_layout.setTitle(_translate("GPSForm", "Step 1 - Identification", None))
        self.numer_label.setText(_translate("GPSForm", "Car Number", None))
        self.color_label.setText(_translate("GPSForm", "Car Color", None))
        self.sync_layout.setTitle(_translate("GPSForm", "Step 2 - Synchronize", None))
        self.time_label.setText(_translate("GPSForm", "Car Start Time", None))
        self.time_input.setDisplayFormat(_translate("GPSForm", "HH:mm", None))

