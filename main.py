#!/usr/bin/env python
from PyQt4 import QtGui, QtCore
from MainSkel import Ui_MainWindow
import sys
import signal
from widgets import Sidebar as sb
from widgets import ImageWidgets as img
from widgets.GZCQWidgets import QLabelButton
from os.path import dirname, join


FILE_DPATH = dirname(__file__)
BUTTON_SIZE = 150
TOGGLE_BUTTON_CAM = join(FILE_DPATH, "assets/icons/icon_camera.png")
TOGGLE_BUTTON_GPS = join(FILE_DPATH, "assets/icons/icon_gps.png")
TOGGLE_BITMAP = join(FILE_DPATH, "assets/icons/toggle_bitmap.png")


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.toggle_button_cam_ic = QtGui.QPixmap(TOGGLE_BUTTON_CAM).scaled(BUTTON_SIZE, BUTTON_SIZE)
        self.toggle_button_gps_ic = QtGui.QPixmap(TOGGLE_BUTTON_GPS).scaled(BUTTON_SIZE, BUTTON_SIZE)
        self.toggle_button_bitmap = QtGui.QPixmap(TOGGLE_BITMAP).scaled(BUTTON_SIZE, BUTTON_SIZE)
        self.initWidgets()
        self.initConnect()

        self.setWindowTitle("Great Zebra Count 2015")
        # self.setStyleSheet("background-color: white;")

        self.shortcutFull = QtGui.QShortcut(self)
        self.shortcutFull.setKey(QtGui.QKeySequence('F11'))
        self.shortcutFull.setContext(QtCore.Qt.ApplicationShortcut)
        self.shortcutFull.activated.connect(self.handleFullScreen)

    def handleFullScreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def resizeEvent(self, ev):
        self.toggle_button.move(self.width() - self.toggle_button.width(), 0)

    def initWidgets(self):
        self.sidebar = sb.Sidebar(parent=self)
        self.sidebar.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        self.sidebar_space.addWidget(self.sidebar)
        self.current_display = 0  # 0 -> image display, 1 -> gps display
        self.img_display = img.selection_group()
        self.display_space.addWidget(self.img_display)

        self.toggle_button = QLabelButton(icon1=self.toggle_button_cam_ic, icon2=self.toggle_button_gps_ic, bitmap=self.toggle_button_bitmap)
        self.toggle_button.resize(BUTTON_SIZE, BUTTON_SIZE)
        #self.toggle_button.setStyleSheet("background-color: red;")
        self.toggle_button.move(self.width(), 0)
        self.toggle_button.setParent(self.centralWidget())
        self.toggle_button.show()

    def initConnect(self):
        self.toggle_button.clicked.connect(self.switchWidgets)

    def switchWidgets(self):
        self.current_display = (self.current_display + 1) % 2
        self.sidebar.switchWidgets(self.current_display)
        if self.current_display == 0:
            self.img_display.show()
            #self.gps_display.hide()
        else:
            self.img_display.hide()
            #self.gps_display.show()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    window.show()
    sys.exit(app.exec_())
