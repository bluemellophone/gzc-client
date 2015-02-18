# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Main.ui'
#
# Created: Wed Feb 18 17:08:55 2015
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.layout = QtGui.QHBoxLayout()
        self.layout.setObjectName(_fromUtf8("layout"))
        self.sidebar_space = QtGui.QVBoxLayout()
        self.sidebar_space.setObjectName(_fromUtf8("sidebar_space"))
        self.layout.addLayout(self.sidebar_space)
        self.divider = QtGui.QFrame(self.centralwidget)
        self.divider.setFrameShape(QtGui.QFrame.VLine)
        self.divider.setFrameShadow(QtGui.QFrame.Sunken)
        self.divider.setObjectName(_fromUtf8("divider"))
        self.layout.addWidget(self.divider)
        self.right_layout = QtGui.QVBoxLayout()
        self.right_layout.setObjectName(_fromUtf8("right_layout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.image_tab = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image_tab.sizePolicy().hasHeightForWidth())
        self.image_tab.setSizePolicy(sizePolicy)
        self.image_tab.setCheckable(True)
        self.image_tab.setChecked(True)
        self.image_tab.setObjectName(_fromUtf8("image_tab"))
        self.horizontalLayout.addWidget(self.image_tab)
        self.gps_tab = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gps_tab.sizePolicy().hasHeightForWidth())
        self.gps_tab.setSizePolicy(sizePolicy)
        self.gps_tab.setCheckable(True)
        self.gps_tab.setObjectName(_fromUtf8("gps_tab"))
        self.horizontalLayout.addWidget(self.gps_tab)
        self.right_layout.addLayout(self.horizontalLayout)
        self.display_space = QtGui.QHBoxLayout()
        self.display_space.setObjectName(_fromUtf8("display_space"))
        self.right_layout.addLayout(self.display_space)
        self.layout.addLayout(self.right_layout)
        self.horizontalLayout_2.addLayout(self.layout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuOptions = QtGui.QMenu(self.menubar)
        self.menuOptions.setObjectName(_fromUtf8("menuOptions"))
        MainWindow.setMenuBar(self.menubar)
        self.actionSpecify_Domain = QtGui.QAction(MainWindow)
        self.actionSpecify_Domain.setObjectName(_fromUtf8("actionSpecify_Domain"))
        self.actionSpecify_Filepaths = QtGui.QAction(MainWindow)
        self.actionSpecify_Filepaths.setObjectName(_fromUtf8("actionSpecify_Filepaths"))
        self.actionManually_Select_Images = QtGui.QAction(MainWindow)
        self.actionManually_Select_Images.setObjectName(_fromUtf8("actionManually_Select_Images"))
        self.actionManually_Select_GPS_Data = QtGui.QAction(MainWindow)
        self.actionManually_Select_GPS_Data.setObjectName(_fromUtf8("actionManually_Select_GPS_Data"))
        self.menuOptions.addAction(self.actionSpecify_Domain)
        self.menuOptions.addAction(self.actionSpecify_Filepaths)
        self.menuOptions.addSeparator()
        self.menuOptions.addAction(self.actionManually_Select_Images)
        self.menuOptions.addAction(self.actionManually_Select_GPS_Data)
        self.menubar.addAction(self.menuOptions.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.image_tab.setText(_translate("MainWindow", "PushButton", None))
        self.gps_tab.setText(_translate("MainWindow", "GPS", None))
        self.menuOptions.setTitle(_translate("MainWindow", "File", None))
        self.actionSpecify_Domain.setText(_translate("MainWindow", "Specify Domain", None))
        self.actionSpecify_Filepaths.setText(_translate("MainWindow", "Specify Filepaths", None))
        self.actionManually_Select_Images.setText(_translate("MainWindow", "Manually Select Images", None))
        self.actionManually_Select_GPS_Data.setText(_translate("MainWindow", "Manually Select GPS Data", None))

