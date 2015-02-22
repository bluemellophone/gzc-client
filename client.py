#!/usr/bin/env python
from PyQt4 import QtGui, QtCore
import sys
import signal
from widgets import Sidebar as sb
from widgets import ImageWidgets as img
# from widgets import GPSWidgets as gps
from widgets.MainSkel import Ui_MainWindow
from widgets.GZCQWidgets import QLabelButton


BUTTON_SIZE = 100
TOGGLE_BUTTON_CAM = "assets/icons/icon_camera_small.png"
TOGGLE_BUTTON_GPS = "assets/icons/icon_gps_small.png"
TOGGLE_BITMAP     = "assets/icons/bitmap_toggle_small.png"


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        # Load toggle button icons and bitmap
        self.toggle_button_cam_ic = QtGui.QPixmap(TOGGLE_BUTTON_CAM).scaled(BUTTON_SIZE, BUTTON_SIZE)
        self.toggle_button_gps_ic = QtGui.QPixmap(TOGGLE_BUTTON_GPS).scaled(BUTTON_SIZE, BUTTON_SIZE)
        self.toggle_button_bitmap = QtGui.QPixmap(TOGGLE_BITMAP).scaled(BUTTON_SIZE, BUTTON_SIZE)
        # Init
        self.setupUi(self)
        self.initWidgets()
        self.initConnect()
        self.initVisuals()

    def initWidgets(self):
        # Init displays
        self.img_display = img.selection_group()
        self.display_space.addWidget(self.img_display)
        # Init sidebar (must happen second)
        self.currentDisplay = 0  # 0 -> image display, 1 -> gps display
        self.sidebar = sb.Sidebar(parent=self)
        self.sidebar.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        self.sidebar_space.addWidget(self.sidebar)
        # Init toggle button
        self.toggle_button = QLabelButton(
            icon1=self.toggle_button_cam_ic,
            icon2=self.toggle_button_gps_ic,
            bitmap=self.toggle_button_bitmap
        )
        self.toggle_button.resize(BUTTON_SIZE, BUTTON_SIZE)
        self.toggle_button.move(self.width(), 0)
        self.toggle_button.setParent(self.centralWidget())
        self.toggle_button.show()

    def initConnect(self):
        self.toggle_button.clicked.connect(self.switchWidgets)
        # Shortcut for fullscreen
        self.shortcutFull = QtGui.QShortcut(self)
        self.shortcutFull.setKey(QtGui.QKeySequence('F11'))
        self.shortcutFull.setContext(QtCore.Qt.ApplicationShortcut)
        self.shortcutFull.activated.connect(self.handleFullScreen)

    def initVisuals(self):
        # Set window title
        self.setWindowTitle("Great Zebra Count 2015")
        # self.setStyleSheet("background-color: white;")

    # Slots
    def handleFullScreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def resizeEvent(self, ev):
        self.toggle_button.move(self.width() - self.toggle_button.width(), 0)

    # Functions
    def allImagesSelected(self):
        return self.img_display.all_images_selected()

    def switchWidgets(self):
        self.currentDisplay = (self.currentDisplay + 1) % 2
        self.sidebar.clear()
        if self.currentDisplay == 0:
            self.img_display.show()
            #self.gps_display.hide()
        elif self.currentDisplay == 1:
            self.img_display.hide()
            #self.gps_display.show()

    def clearImageDisplay(self):
        self.img_display.clear()
        pass

    def clearGPSDisplay(self):
        # self.gps_display.clear()
        pass

    def clear(self):
        self.clearImageDisplay()
        self.clearGPSDisplay()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    window.show()
    sys.exit(app.exec_())
