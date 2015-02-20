# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Sidebar.ui'
#
# Created: Thu Feb 19 13:48:21 2015
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

class Ui_Sidebar(object):
    def setupUi(self, Sidebar):
        Sidebar.setObjectName(_fromUtf8("Sidebar"))
        Sidebar.resize(282, 598)
        Sidebar.setMinimumSize(QtCore.QSize(0, 0))
        Sidebar.setBaseSize(QtCore.QSize(100, 100))
        font = QtGui.QFont()
        font.setPointSize(12)
        Sidebar.setFont(font)
        self.horizontalLayout = QtGui.QHBoxLayout(Sidebar)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.layout = QtGui.QVBoxLayout()
        self.layout.setObjectName(_fromUtf8("layout"))
        self.logo_layout = QtGui.QHBoxLayout()
        self.logo_layout.setObjectName(_fromUtf8("logo_layout"))
        self.logo_1 = QtGui.QLabel(Sidebar)
        self.logo_1.setText(_fromUtf8(""))
        self.logo_1.setObjectName(_fromUtf8("logo_1"))
        self.logo_layout.addWidget(self.logo_1)
        self.logo_2 = QtGui.QLabel(Sidebar)
        self.logo_2.setText(_fromUtf8(""))
        self.logo_2.setObjectName(_fromUtf8("logo_2"))
        self.logo_layout.addWidget(self.logo_2)
        self.layout.addLayout(self.logo_layout)
        self.form = QtGui.QVBoxLayout()
        self.form.setObjectName(_fromUtf8("form"))
        self.layout.addLayout(self.form)
        self.frame = QtGui.QFrame(Sidebar)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.layout.addWidget(self.frame)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.layout.addItem(spacerItem)
        self.button_layout = QtGui.QHBoxLayout()
        self.button_layout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.button_layout.setObjectName(_fromUtf8("button_layout"))
        self.submit = QtGui.QPushButton(Sidebar)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.submit.sizePolicy().hasHeightForWidth())
        self.submit.setSizePolicy(sizePolicy)
        self.submit.setMinimumSize(QtCore.QSize(0, 70))
        self.submit.setMaximumSize(QtCore.QSize(16777215, 70))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.submit.setFont(font)
        self.submit.setObjectName(_fromUtf8("submit"))
        self.button_layout.addWidget(self.submit)
        self.clear = QtGui.QPushButton(Sidebar)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clear.sizePolicy().hasHeightForWidth())
        self.clear.setSizePolicy(sizePolicy)
        self.clear.setMinimumSize(QtCore.QSize(0, 70))
        self.clear.setMaximumSize(QtCore.QSize(16777215, 70))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.clear.setFont(font)
        self.clear.setAutoFillBackground(False)
        self.clear.setStyleSheet(_fromUtf8("color: red;"))
        self.clear.setAutoDefault(False)
        self.clear.setDefault(False)
        self.clear.setFlat(False)
        self.clear.setObjectName(_fromUtf8("clear"))
        self.button_layout.addWidget(self.clear)
        self.button_layout.setStretch(0, 5)
        self.button_layout.setStretch(1, 1)
        self.layout.addLayout(self.button_layout)
        self.split_1 = QtGui.QFrame(Sidebar)
        self.split_1.setFrameShape(QtGui.QFrame.HLine)
        self.split_1.setFrameShadow(QtGui.QFrame.Sunken)
        self.split_1.setObjectName(_fromUtf8("split_1"))
        self.layout.addWidget(self.split_1)
        self.sidebar_status = QtGui.QLabel(Sidebar)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.sidebar_status.setFont(font)
        self.sidebar_status.setStyleSheet(_fromUtf8("color: #666;"))
        self.sidebar_status.setText(_fromUtf8(""))
        self.sidebar_status.setObjectName(_fromUtf8("sidebar_status"))
        self.layout.addWidget(self.sidebar_status)
        self.layout.setStretch(4, 2)
        self.horizontalLayout.addLayout(self.layout)

        self.retranslateUi(Sidebar)
        QtCore.QMetaObject.connectSlotsByName(Sidebar)

    def retranslateUi(self, Sidebar):
        Sidebar.setWindowTitle(_translate("Sidebar", "Form", None))
        self.submit.setText(_translate("Sidebar", "Import", None))
        self.clear.setText(_translate("Sidebar", "Clear", None))

