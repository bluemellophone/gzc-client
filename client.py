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
        self.imageDisplay = img.selection_group()
        self.displaySpace.addWidget(self.imageDisplay)
        # Init sidebar (must happen second)
        self.currentDisplay = 0  # 0 -> image display, 1 -> gps display
        self.sidebar = sb.Sidebar(parent=self)
        self.sidebar.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        self.sidebarSpace.addWidget(self.sidebar)
        # Init toggle button
        self.toggleButton = QLabelButton(
            icon1=self.toggle_button_cam_ic,
            icon2=self.toggle_button_gps_ic,
            bitmap=self.toggle_button_bitmap
        )
        self.toggleButton.resize(BUTTON_SIZE, BUTTON_SIZE)
        self.toggleButton.move(self.width(), 0)
        self.toggleButton.setParent(self.centralWidget())
        self.toggleButton.show()

    def initConnect(self):
        self.toggleButton.clicked.connect(self.switchWidgets)
        self.actionSpecifyDomain.triggered.connect(self.specifyDomain)
        self.actionSpecifyFilepaths.triggered.connect(self.specifyFilepaths)
        self.actionManuallySelectImages.triggered.connect(self.manuallySelectImages)
        self.actionManuallySelectGPS.triggered.connect(self.manuallySelectGPS)
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
        self.toggleButton.move(self.width() - self.toggleButton.width(), 0)

    def specifyDomain(self, checked):
        print('specifyDomain')

    def specifyFilepaths(self, checked):
        print('specifyFilepaths')

    def manuallySelectImages(self, checked):
        print('manuallySelectImages')

    def manuallySelectGPS(self, checked):
        print('manuallySelectGPS')

    # Functions
    def allImagesSelected(self):
        return self.imageDisplay.allImagesSelected()

    def switchWidgets(self):
        self.currentDisplay = (self.currentDisplay + 1) % 2
        self.sidebar.clear()
        if self.currentDisplay == 0:
            self.imageDisplay.show()
            #self.gpsDisplay.hide()
        elif self.currentDisplay == 1:
            self.imageDisplay.hide()
            #self.gpsDisplay.show()

    def clearImageDisplay(self):
        self.imageDisplay.clear()
        pass

    def clearGPSDisplay(self):
        # self.gpsDisplay.clear()
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
