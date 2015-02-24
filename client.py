#!/usr/bin/env python
from PyQt4 import QtGui, QtCore
import sys
from os.path import abspath, join, expanduser
import signal
import widgets  # NOQA
import numpy as np # NOQA
from widgets import Sidebar as sb
from widgets import ImageWidgets as img
from widgets import GPSWidgets as gps
from widgets.MainSkel import Ui_MainWindow
from widgets.GZCQWidgets import QLabelButton
from clientfuncs import ex_deco, resource_path
import simplejson as json
import requests

TOGGLE_BUTTON_SIZE = 100
DEFAULT_DOMAIN    = 'http://localhost:5000'
DEFAULT_PATH      = abspath(expanduser(join('~', 'Desktop', 'gzc-client-data')))
TOGGLE_BUTTON_CAM = resource_path(join('assets', 'icons', 'icon_camera_small.png'))
TOGGLE_BUTTON_GPS = resource_path(join('assets', 'icons', 'icon_gps_small.png'))
TOGGLE_BITMAP     = resource_path(join('assets', 'icons', 'bitmap_toggle_small.png'))


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        # Load toggle button icons and bitmap
        self.domain = DEFAULT_DOMAIN
        self.path_list = [DEFAULT_PATH]
        self.toggle_button_cam_ic = QtGui.QPixmap(TOGGLE_BUTTON_CAM).scaled(TOGGLE_BUTTON_SIZE, TOGGLE_BUTTON_SIZE)
        self.toggle_button_gps_ic = QtGui.QPixmap(TOGGLE_BUTTON_GPS).scaled(TOGGLE_BUTTON_SIZE, TOGGLE_BUTTON_SIZE)
        self.toggle_button_bitmap = QtGui.QPixmap(TOGGLE_BITMAP).scaled(TOGGLE_BUTTON_SIZE, TOGGLE_BUTTON_SIZE)
        # Init
        self.setupUi(self)
        self.initWidgets()
        self.initConnect()
        self.initVisuals()
        self.clear()

    def initWidgets(self):
        # Init displays
        self.imageDisplay = img.selection_group(self)
        self.gpsDisplay = gps.gps_map(self)
        self.displaySpace.addWidget(self.imageDisplay)
        self.displaySpace.addWidget(self.gpsDisplay)
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
        self.toggleButton.resize(TOGGLE_BUTTON_SIZE, TOGGLE_BUTTON_SIZE)
        self.toggleButton.move(self.width(), 0)
        self.toggleButton.setParent(self.centralWidget())
        self.toggleButton.show()
        # Domain input
        self.domainInput = QtGui.QInputDialog()
        self.domainInput.setLabelText(QtCore.QString('Enter server domain'))
        self.pathInput = QtGui.QInputDialog()
        self.pathInput.setLabelText(QtCore.QString('Enter copy paths'))

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
        # Menu items
        self.domainInput.accepted.connect(self.domainChanged)
        self.pathInput.accepted.connect(self.pathChanged)
        self.domainInput.textValueChanged.connect(self.checkServerResponse)

    def initVisuals(self):
        # Set window title
        self.setWindowTitle('Great Zebra Count 2015')
        # self.setStyleSheet('background-color: white;')

    # Slots
    def handleFullScreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def resizeEvent(self, ev):
        self.toggleButton.move(self.width() - self.toggleButton.width(), 0)
        self.imageDisplay.triggerResize()

    def specifyDomain(self, checked):
        self.domainInput.setTextValue(self.domain)
        self.domainInput.show()

    def specifyFilepaths(self, checked):
        self.pathInput.setTextValue(','.join(self.path_list))
        self.pathInput.show()

    def manuallySelectImages(self, checked):
        dialog = QtGui.QFileDialog()
        dialog.setFileMode(QtGui.QFileDialog.ExistingFiles)
        qFiles = dialog.getOpenFileNames(self, 'Select image files')
        # convert QStringList to a python list of strings
        files = [str(f) for f in qFiles]
        self.sidebar.imagesSelectedOverride(files)

    def manuallySelectGPS(self, checked):
        dialog = QtGui.QFileDialog()
        dialog.setFileMode(QtGui.QFileDialog.ExistingFile)
        fname = str(dialog.getOpenFileName(self, 'Select GPX file'))
        self.sidebar.copyGPS(fname)

    def checkServerResponse(self, value):
        self.domainInput.setLabelText(QtCore.QString('Enter server domain'))
        value = str(value)
        try:
            r = requests.get(value + '/status', timeout=0.1)
            response = json.loads(r.text)
            if response['status']['code'] == 0:
                self.domainInput.setLabelText(QtCore.QString('Enter server domain - Valid Server Response'))
        except requests.exceptions.ConnectionError:
            pass

    # Functions
    @ex_deco
    def domainChanged(self):
        self.domain = str(self.domainInput.textValue())

    @ex_deco
    def pathChanged(self):
        path_str = str(self.pathInput.textValue())
        self.path_list = map(abspath, path_str.split(','))

    @ex_deco
    def allImagesSelected(self):
        return self.imageDisplay.all_images_selected()

    @ex_deco
    def switchWidgets(self):
        self.currentDisplay = (self.currentDisplay + 1) % 2
        self.clear()

    @ex_deco
    def displayGPXTrack(self, gpx_track):
        self.gpsDisplay.clear(gpx_track)

    @ex_deco
    def clearSidebar(self):
        self.sidebar.clear()

    @ex_deco
    def clearImageDisplay(self):
        self.imageDisplay.clear()

    @ex_deco
    def clearGPSDisplay(self):
        self.gpsDisplay.clear()

    @ex_deco
    def clear(self):
        self.imageDisplay.hide()
        self.gpsDisplay.hide()
        self.actionManuallySelectImages.setEnabled(False)
        self.actionManuallySelectGPS.setEnabled(False)
        # Show correct display
        if self.currentDisplay == 0:
            self.imageDisplay.show()
            self.actionManuallySelectImages.setEnabled(True)
        elif self.currentDisplay == 1:
            self.gpsDisplay.show()
            self.actionManuallySelectGPS.setEnabled(True)
        # Clear children
        self.clearSidebar()
        self.clearImageDisplay()
        self.clearGPSDisplay()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    window.show()
    sys.exit(app.exec_())
