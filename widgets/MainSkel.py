# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Main.ui'
#
# Created: Fri Feb 27 22:16:41 2015
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1400, 872)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(1400, 850))
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.layout = QtGui.QHBoxLayout()
        self.layout.setObjectName(_fromUtf8("layout"))
        self.sidebarSpace = QtGui.QVBoxLayout()
        self.sidebarSpace.setObjectName(_fromUtf8("sidebarSpace"))
        self.layout.addLayout(self.sidebarSpace)
        self.divider = QtGui.QFrame(self.centralwidget)
        self.divider.setFrameShape(QtGui.QFrame.VLine)
        self.divider.setFrameShadow(QtGui.QFrame.Sunken)
        self.divider.setObjectName(_fromUtf8("divider"))
        self.layout.addWidget(self.divider)
        self.displaySpace = QtGui.QVBoxLayout()
        self.displaySpace.setObjectName(_fromUtf8("displaySpace"))
        self.layout.addLayout(self.displaySpace)
        self.horizontalLayout_2.addLayout(self.layout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1400, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuOptions = QtGui.QMenu(self.menubar)
        self.menuOptions.setObjectName(_fromUtf8("menuOptions"))
        MainWindow.setMenuBar(self.menubar)
        self.actionSpecifyDomain = QtGui.QAction(MainWindow)
        self.actionSpecifyDomain.setObjectName(_fromUtf8("actionSpecifyDomain"))
        self.actionSpecifyFilepaths = QtGui.QAction(MainWindow)
        self.actionSpecifyFilepaths.setObjectName(_fromUtf8("actionSpecifyFilepaths"))
        self.actionManuallySelectImages = QtGui.QAction(MainWindow)
        self.actionManuallySelectImages.setObjectName(_fromUtf8("actionManuallySelectImages"))
        self.actionManuallySelectGPS = QtGui.QAction(MainWindow)
        self.actionManuallySelectGPS.setObjectName(_fromUtf8("actionManuallySelectGPS"))
        self.menuOptions.addAction(self.actionSpecifyDomain)
        self.menuOptions.addAction(self.actionSpecifyFilepaths)
        self.menuOptions.addSeparator()
        self.menuOptions.addAction(self.actionManuallySelectImages)
        self.menuOptions.addAction(self.actionManuallySelectGPS)
        self.menubar.addAction(self.menuOptions.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.menuOptions.setTitle(_translate("MainWindow", "File", None))
        self.actionSpecifyDomain.setText(_translate("MainWindow", "Specify Domain", None))
        self.actionSpecifyFilepaths.setText(_translate("MainWindow", "Specify Filepaths", None))
        self.actionManuallySelectImages.setText(_translate("MainWindow", "Manually Select Images", None))
        self.actionManuallySelectGPS.setText(_translate("MainWindow", "Manually Select GPX File", None))

