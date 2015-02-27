# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Sidebar.ui'
#
# Created: Fri Feb 27 20:46:19 2015
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
        Sidebar.resize(447, 763)
        Sidebar.setMinimumSize(QtCore.QSize(447, 0))
        Sidebar.setBaseSize(QtCore.QSize(100, 100))
        font = QtGui.QFont()
        font.setPointSize(12)
        Sidebar.setFont(font)
        self.horizontalLayout = QtGui.QHBoxLayout(Sidebar)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.layout = QtGui.QVBoxLayout()
        self.layout.setObjectName(_fromUtf8("layout"))
        self.logoLayout = QtGui.QHBoxLayout()
        self.logoLayout.setObjectName(_fromUtf8("logoLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.logoLayout.addItem(spacerItem)
        self.logo = QtGui.QLabel(Sidebar)
        self.logo.setText(_fromUtf8(""))
        self.logo.setObjectName(_fromUtf8("logo"))
        self.logoLayout.addWidget(self.logo)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.logoLayout.addItem(spacerItem1)
        self.layout.addLayout(self.logoLayout)
        self.form = QtGui.QVBoxLayout()
        self.form.setObjectName(_fromUtf8("form"))
        self.layout.addLayout(self.form)
        self.buttonLayout = QtGui.QHBoxLayout()
        self.buttonLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.buttonLayout.setObjectName(_fromUtf8("buttonLayout"))
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
        self.buttonLayout.addWidget(self.submitButton)
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
        self.buttonLayout.addWidget(self.clearButton)
        self.buttonLayout.setStretch(0, 5)
        self.buttonLayout.setStretch(1, 1)
        self.layout.addLayout(self.buttonLayout)
        self.split1 = QtGui.QFrame(Sidebar)
        self.split1.setFrameShape(QtGui.QFrame.HLine)
        self.split1.setFrameShadow(QtGui.QFrame.Sunken)
        self.split1.setObjectName(_fromUtf8("split1"))
        self.layout.addWidget(self.split1)
        self.sidebarStatus = QtGui.QLabel(Sidebar)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.sidebarStatus.setFont(font)
        self.sidebarStatus.setStyleSheet(_fromUtf8("color: #666;"))
        self.sidebarStatus.setText(_fromUtf8(""))
        self.sidebarStatus.setObjectName(_fromUtf8("sidebarStatus"))
        self.layout.addWidget(self.sidebarStatus)
        self.layout.setStretch(1, 5)
        self.layout.setStretch(2, 1)
        self.horizontalLayout.addLayout(self.layout)

        self.retranslateUi(Sidebar)
        QtCore.QMetaObject.connectSlotsByName(Sidebar)

    def retranslateUi(self, Sidebar):
        Sidebar.setWindowTitle(_translate("Sidebar", "Form", None))
        self.submitButton.setText(_translate("Sidebar", "Import", None))
        self.clearButton.setText(_translate("Sidebar", "Clear", None))

