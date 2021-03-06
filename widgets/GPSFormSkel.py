# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GPSForm.ui'
#
# Created: Sat Feb 28 03:41:03 2015
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
        GPSForm.resize(539, 494)
        font = QtGui.QFont()
        font.setPointSize(12)
        GPSForm.setFont(font)
        self.verticalLayout = QtGui.QVBoxLayout(GPSForm)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.layout = QtGui.QVBoxLayout()
        self.layout.setSpacing(15)
        self.layout.setObjectName(_fromUtf8("layout"))
        self.idLayout = QtGui.QGroupBox(GPSForm)
        self.idLayout.setMinimumSize(QtCore.QSize(0, 120))
        self.idLayout.setMaximumSize(QtCore.QSize(16777215, 120))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.idLayout.setFont(font)
        self.idLayout.setStyleSheet(_fromUtf8("font-size:20px;color:#333;"))
        self.idLayout.setFlat(False)
        self.idLayout.setObjectName(_fromUtf8("idLayout"))
        self.formLayout_4 = QtGui.QFormLayout(self.idLayout)
        self.formLayout_4.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_4.setObjectName(_fromUtf8("formLayout_4"))
        self.numerLabel = QtGui.QLabel(self.idLayout)
        self.numerLabel.setMinimumSize(QtCore.QSize(159, 0))
        self.numerLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.numerLabel.setObjectName(_fromUtf8("numerLabel"))
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.LabelRole, self.numerLabel)
        self.numberInput = QtGui.QComboBox(self.idLayout)
        self.numberInput.setMinimumSize(QtCore.QSize(0, 30))
        self.numberInput.setObjectName(_fromUtf8("numberInput"))
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.FieldRole, self.numberInput)
        self.colorLabel = QtGui.QLabel(self.idLayout)
        self.colorLabel.setMinimumSize(QtCore.QSize(159, 0))
        self.colorLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.colorLabel.setObjectName(_fromUtf8("colorLabel"))
        self.formLayout_4.setWidget(2, QtGui.QFormLayout.LabelRole, self.colorLabel)
        self.colorInputContainer = QtGui.QVBoxLayout()
        self.colorInputContainer.setObjectName(_fromUtf8("colorInputContainer"))
        self.formLayout_4.setLayout(2, QtGui.QFormLayout.FieldRole, self.colorInputContainer)
        self.layout.addWidget(self.idLayout)
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        self.layout.addItem(spacerItem)
        self.syncLayout = QtGui.QGroupBox(GPSForm)
        self.syncLayout.setMinimumSize(QtCore.QSize(0, 122))
        self.syncLayout.setMaximumSize(QtCore.QSize(16777215, 122))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.syncLayout.setFont(font)
        self.syncLayout.setStyleSheet(_fromUtf8("font-size:20px;color:#333;"))
        self.syncLayout.setFlat(False)
        self.syncLayout.setObjectName(_fromUtf8("syncLayout"))
        self.formLayout_6 = QtGui.QFormLayout(self.syncLayout)
        self.formLayout_6.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_6.setObjectName(_fromUtf8("formLayout_6"))
        self.timeLabel = QtGui.QLabel(self.syncLayout)
        self.timeLabel.setMinimumSize(QtCore.QSize(159, 0))
        self.timeLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.timeLabel.setObjectName(_fromUtf8("timeLabel"))
        self.formLayout_6.setWidget(0, QtGui.QFormLayout.LabelRole, self.timeLabel)
        self.label = QtGui.QLabel(self.syncLayout)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout_6.setWidget(2, QtGui.QFormLayout.LabelRole, self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.timeHour = QtGui.QComboBox(self.syncLayout)
        self.timeHour.setMaximumSize(QtCore.QSize(100, 16777215))
        self.timeHour.setObjectName(_fromUtf8("timeHour"))
        self.horizontalLayout.addWidget(self.timeHour)
        self.timeMinute = QtGui.QComboBox(self.syncLayout)
        self.timeMinute.setMaximumSize(QtCore.QSize(100, 16777215))
        self.timeMinute.setObjectName(_fromUtf8("timeMinute"))
        self.horizontalLayout.addWidget(self.timeMinute)
        self.formLayout_6.setLayout(0, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.trackNumber = QtGui.QComboBox(self.syncLayout)
        self.trackNumber.setObjectName(_fromUtf8("trackNumber"))
        self.formLayout_6.setWidget(2, QtGui.QFormLayout.FieldRole, self.trackNumber)
        self.layout.addWidget(self.syncLayout)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.layout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.layout)

        self.retranslateUi(GPSForm)
        QtCore.QMetaObject.connectSlotsByName(GPSForm)

    def retranslateUi(self, GPSForm):
        GPSForm.setWindowTitle(_translate("GPSForm", "Form", None))
        self.idLayout.setTitle(_translate("GPSForm", "Step 1 - Identification", None))
        self.numerLabel.setText(_translate("GPSForm", "Car Number", None))
        self.colorLabel.setText(_translate("GPSForm", "Car Color", None))
        self.syncLayout.setTitle(_translate("GPSForm", "Step 2 - Synchronize", None))
        self.timeLabel.setText(_translate("GPSForm", "Car Start Time", None))
        self.label.setText(_translate("GPSForm", "Track Number", None))

