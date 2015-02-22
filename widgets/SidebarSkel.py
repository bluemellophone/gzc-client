# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Sidebar.ui'
#
# Created: Sun Feb 22 13:07:33 2015
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

class Ui_Sidebar(object):
    def setupUi(self, Sidebar):
        Sidebar.setObjectName(_fromUtf8("Sidebar"))
        Sidebar.resize(364, 763)
        Sidebar.setMinimumSize(QtCore.QSize(0, 0))
        Sidebar.setBaseSize(QtCore.QSize(100, 100))
        font = QtGui.QFont()
        font.setPointSize(12)
        Sidebar.setFont(font)
        self.horizontalLayout = QtGui.QHBoxLayout(Sidebar)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.layout = QtGui.QVBoxLayout()
        self.layout.setObjectName(_fromUtf8("layout"))
        self.logo_layout_wide = QtGui.QHBoxLayout()
        self.logo_layout_wide.setObjectName(_fromUtf8("logo_layout_wide"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.logo_layout_wide.addItem(spacerItem)
        self.logo_0 = QtGui.QLabel(Sidebar)
        self.logo_0.setText(_fromUtf8(""))
        self.logo_0.setObjectName(_fromUtf8("logo_0"))
        self.logo_layout_wide.addWidget(self.logo_0)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.logo_layout_wide.addItem(spacerItem1)
        self.layout.addLayout(self.logo_layout_wide)
        self.logo_layout = QtGui.QHBoxLayout()
        self.logo_layout.setObjectName(_fromUtf8("logo_layout"))
        self.logo_1 = QtGui.QLabel(Sidebar)
        self.logo_1.setText(_fromUtf8(""))
        self.logo_1.setObjectName(_fromUtf8("logo_1"))
        self.logo_layout.addWidget(self.logo_1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.logo_2 = QtGui.QLabel(Sidebar)
        self.logo_2.setText(_fromUtf8(""))
        self.logo_2.setObjectName(_fromUtf8("logo_2"))
        self.logo_layout.addWidget(self.logo_2, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.layout.addLayout(self.logo_layout)
        self.form = QtGui.QVBoxLayout()
        self.form.setObjectName(_fromUtf8("form"))
        self.layout.addLayout(self.form)
        self.button_layout = QtGui.QHBoxLayout()
        self.button_layout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.button_layout.setObjectName(_fromUtf8("button_layout"))
        self.submitButton = QtGui.QPushButton(Sidebar)
        self.submitButton.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.submitButton.sizePolicy().hasHeightForWidth())
        self.submitButton.setSizePolicy(sizePolicy)
        self.submitButton.setMinimumSize(QtCore.QSize(0, 100))
        self.submitButton.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.submitButton.setFont(font)
        self.submitButton.setStyleSheet(_fromUtf8("font-size:32px;"))
        self.submitButton.setIconSize(QtCore.QSize(24, 24))
        self.submitButton.setFlat(False)
        self.submitButton.setObjectName(_fromUtf8("submitButton"))
        self.button_layout.addWidget(self.submitButton)
        self.clearButton = QtGui.QPushButton(Sidebar)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clearButton.sizePolicy().hasHeightForWidth())
        self.clearButton.setSizePolicy(sizePolicy)
        self.clearButton.setMinimumSize(QtCore.QSize(0, 100))
        self.clearButton.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.clearButton.setFont(font)
        self.clearButton.setAutoFillBackground(False)
        self.clearButton.setStyleSheet(_fromUtf8("color: red; font-size:24px;"))
        self.clearButton.setIconSize(QtCore.QSize(28, 28))
        self.clearButton.setAutoDefault(False)
        self.clearButton.setDefault(False)
        self.clearButton.setFlat(False)
        self.clearButton.setObjectName(_fromUtf8("clearButton"))
        self.button_layout.addWidget(self.clearButton)
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
        self.layout.setStretch(0, 1)
        self.layout.setStretch(2, 5)
        self.layout.setStretch(3, 1)
        self.horizontalLayout.addLayout(self.layout)

        self.retranslateUi(Sidebar)
        QtCore.QMetaObject.connectSlotsByName(Sidebar)

    def retranslateUi(self, Sidebar):
        Sidebar.setWindowTitle(_translate("Sidebar", "Form", None))
        self.submitButton.setText(_translate("Sidebar", "Import", None))
        self.clearButton.setText(_translate("Sidebar", "Clear", None))

