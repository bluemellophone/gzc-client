# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ImageForm.ui'
#
# Created: Fri Feb 27 22:02:00 2015
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

class Ui_ImageForm(object):
    def setupUi(self, ImageForm):
        ImageForm.setObjectName(_fromUtf8("ImageForm"))
        ImageForm.resize(582, 647)
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
        self.driveLayout = QtGui.QGroupBox(ImageForm)
        self.driveLayout.setMinimumSize(QtCore.QSize(0, 129))
        self.driveLayout.setMaximumSize(QtCore.QSize(16777215, 129))
        self.driveLayout.setSizeIncrement(QtCore.QSize(0, 1))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.driveLayout.setFont(font)
        self.driveLayout.setStyleSheet(_fromUtf8("font-size:20px;color:#333;"))
        self.driveLayout.setFlat(False)
        self.driveLayout.setObjectName(_fromUtf8("driveLayout"))
        self.formLayout = QtGui.QFormLayout(self.driveLayout)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setContentsMargins(-1, 12, -1, -1)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.driveBrowse = QtGui.QPushButton(self.driveLayout)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.driveBrowse.sizePolicy().hasHeightForWidth())
        self.driveBrowse.setSizePolicy(sizePolicy)
        self.driveBrowse.setMinimumSize(QtCore.QSize(0, 45))
        self.driveBrowse.setIconSize(QtCore.QSize(20, 20))
        self.driveBrowse.setObjectName(_fromUtf8("driveBrowse"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.SpanningRole, self.driveBrowse)
        self.driveLabel = QtGui.QLabel(self.driveLayout)
        self.driveLabel.setStyleSheet(_fromUtf8("color:#666;"))
        self.driveLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.driveLabel.setWordWrap(False)
        self.driveLabel.setObjectName(_fromUtf8("driveLabel"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.SpanningRole, self.driveLabel)
        self.layout.addWidget(self.driveLayout)
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        self.layout.addItem(spacerItem)
        self.idLayout = QtGui.QGroupBox(ImageForm)
        self.idLayout.setMinimumSize(QtCore.QSize(0, 150))
        self.idLayout.setMaximumSize(QtCore.QSize(16777215, 150))
        self.idLayout.setSizeIncrement(QtCore.QSize(0, 1))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.idLayout.setFont(font)
        self.idLayout.setStyleSheet(_fromUtf8("font-size:20px;color:#333;"))
        self.idLayout.setFlat(False)
        self.idLayout.setCheckable(False)
        self.idLayout.setChecked(False)
        self.idLayout.setObjectName(_fromUtf8("idLayout"))
        self.formLayout_4 = QtGui.QFormLayout(self.idLayout)
        self.formLayout_4.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_4.setContentsMargins(-1, 12, -1, -1)
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
        self.letterLabel = QtGui.QLabel(self.idLayout)
        self.letterLabel.setMinimumSize(QtCore.QSize(159, 0))
        self.letterLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.letterLabel.setObjectName(_fromUtf8("letterLabel"))
        self.formLayout_4.setWidget(3, QtGui.QFormLayout.LabelRole, self.letterLabel)
        self.letterInput = QtGui.QComboBox(self.idLayout)
        self.letterInput.setMinimumSize(QtCore.QSize(0, 30))
        self.letterInput.setObjectName(_fromUtf8("letterInput"))
        self.formLayout_4.setWidget(3, QtGui.QFormLayout.FieldRole, self.letterInput)
        self.colorLabel = QtGui.QLabel(self.idLayout)
        self.colorLabel.setMinimumSize(QtCore.QSize(159, 0))
        self.colorLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.colorLabel.setObjectName(_fromUtf8("colorLabel"))
        self.formLayout_4.setWidget(2, QtGui.QFormLayout.LabelRole, self.colorLabel)
        self.colorInputContainer = QtGui.QVBoxLayout()
        self.colorInputContainer.setObjectName(_fromUtf8("colorInputContainer"))
        self.formLayout_4.setLayout(2, QtGui.QFormLayout.FieldRole, self.colorInputContainer)
        self.layout.addWidget(self.idLayout)
        spacerItem1 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        self.layout.addItem(spacerItem1)
        self.syncLayout = QtGui.QGroupBox(ImageForm)
        self.syncLayout.setMinimumSize(QtCore.QSize(0, 126))
        self.syncLayout.setMaximumSize(QtCore.QSize(16777215, 126))
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
        self.formLayout_6.setContentsMargins(-1, 12, -1, -1)
        self.formLayout_6.setObjectName(_fromUtf8("formLayout_6"))
        self.nameLabel = QtGui.QLabel(self.syncLayout)
        self.nameLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.nameLabel.setObjectName(_fromUtf8("nameLabel"))
        self.formLayout_6.setWidget(0, QtGui.QFormLayout.LabelRole, self.nameLabel)
        self.nameInput = QtGui.QLineEdit(self.syncLayout)
        self.nameInput.setMinimumSize(QtCore.QSize(0, 30))
        self.nameInput.setAlignment(QtCore.Qt.AlignCenter)
        self.nameInput.setObjectName(_fromUtf8("nameInput"))
        self.formLayout_6.setWidget(0, QtGui.QFormLayout.FieldRole, self.nameInput)
        self.timeLabel = QtGui.QLabel(self.syncLayout)
        self.timeLabel.setMinimumSize(QtCore.QSize(159, 0))
        self.timeLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.timeLabel.setObjectName(_fromUtf8("timeLabel"))
        self.formLayout_6.setWidget(1, QtGui.QFormLayout.LabelRole, self.timeLabel)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.timeHour = QtGui.QComboBox(self.syncLayout)
        self.timeHour.setMaximumSize(QtCore.QSize(100, 16777215))
        self.timeHour.setObjectName(_fromUtf8("timeHour"))
        self.horizontalLayout_2.addWidget(self.timeHour)
        self.timeMinute = QtGui.QComboBox(self.syncLayout)
        self.timeMinute.setMaximumSize(QtCore.QSize(100, 16777215))
        self.timeMinute.setObjectName(_fromUtf8("timeMinute"))
        self.horizontalLayout_2.addWidget(self.timeMinute)
        self.formLayout_6.setLayout(1, QtGui.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.layout.addWidget(self.syncLayout)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.layout.addItem(spacerItem2)
        self.horizontalLayout.addLayout(self.layout)

        self.retranslateUi(ImageForm)
        QtCore.QMetaObject.connectSlotsByName(ImageForm)

    def retranslateUi(self, ImageForm):
        ImageForm.setWindowTitle(_translate("ImageForm", "Form", None))
        self.driveLayout.setTitle(_translate("ImageForm", "Step 1 - SD Card", None))
        self.driveBrowse.setText(_translate("ImageForm", "Browse", None))
        self.driveLabel.setText(_translate("ImageForm", "Select a Directory", None))
        self.idLayout.setTitle(_translate("ImageForm", "Step 2 - Identification", None))
        self.numerLabel.setText(_translate("ImageForm", "Car Number", None))
        self.letterLabel.setText(_translate("ImageForm", "Person Letter", None))
        self.colorLabel.setText(_translate("ImageForm", "Car Color", None))
        self.syncLayout.setTitle(_translate("ImageForm", "Step 3 - Synchronize", None))
        self.nameLabel.setText(_translate("ImageForm", "First Image Name", None))
        self.timeLabel.setText(_translate("ImageForm", "First Image Time", None))

