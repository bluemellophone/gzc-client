#!/usr/bin/env python
from __future__ import absolute_import, division, print_function
from PyQt4 import QtGui, QtCore
import sys
from os.path import abspath, join, expanduser, exists
import signal
import widgets  # NOQA
import numpy as np  # NOQA
import utool as ut
from widgets import Sidebar as sb
from widgets import ImageWidgets as img
from widgets import GPSWidgets as gps
from widgets.MainSkel import Ui_MainWindow
from widgets.GZCQWidgets import QLabelButton
from clientfuncs import ex_deco, resource_path
import simplejson as json
import requests
import shutil

RESOURCE_PATH      = ut.get_app_resource_dir('gzc-client')
RESOURCE_CONFIG    = join(RESOURCE_PATH, 'config.json')
TOGGLE_BUTTON_SIZE = 100
# DEFAULT_DOMAIN     = 'http://localhost:5000'
DEFAULT_DOMAIN     = 'http://192.168.0.100:5000'
DEFAULT_PATH       = abspath(expanduser(join('~', 'Desktop', 'gzc-client-data')))
TOGGLE_BUTTON_CAM  = resource_path(join('assets', 'icons', 'icon_camera_small.png'))
TOGGLE_BUTTON_GPS  = resource_path(join('assets', 'icons', 'icon_gps_small.png'))
TOGGLE_BITMAP      = resource_path(join('assets', 'icons', 'bitmap_toggle_small.png'))


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        # Load configuration
        self.loadConfig()
        # Load toggle button icons and bitmap
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
        self.actionLoadDefaultConfig.triggered.connect(self.loadDefaultConfig)
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
        self.checkServerResponse(self.domain)

    def specifyFilepaths(self, checked):
        self.pathInput.setTextValue(','.join(self.backupDestinationPaths))
        self.pathInput.show()

    def manuallySelectImages(self, checked):
        dialog = QtGui.QFileDialog()
        dialog.setFileMode(QtGui.QFileDialog.ExistingFiles)
        qFiles = dialog.getOpenFileNames(self, 'Select image files')
        # convert QStringList to a python list of strings
        files = [str(f) for f in qFiles]
        self.sidebar.imageManualSelection(files)

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

    def loadDefaultConfig(self, checked):
        self.loadConfig(reset=True)

    # Functions
    @ex_deco
    def saveConfig(self, domain=None, backupDestinationPaths=None):
        print('[client] saveConfig')
        if domain is None:
            self.domain = DEFAULT_DOMAIN
        else:
            self.domain = domain
        if backupDestinationPaths is None:
            self.backupDestinationPaths = [DEFAULT_PATH]
        else:
            self.backupDestinationPaths = backupDestinationPaths
        temp = {
            'domain':    self.domain,
            'backupDestinationPaths': self.backupDestinationPaths,
        }
        with open(RESOURCE_CONFIG, 'w') as config:
            json.dump(temp, config)

    def loadConfig(self, reset=False):
        print('[client] loadConfig')
        if reset and exists(RESOURCE_PATH):
            print('[client.loadConfig] Loading default configuration')
            shutil.rmtree(RESOURCE_PATH)
        ut.ensuredir(RESOURCE_PATH)
        if not exists(RESOURCE_CONFIG):
            self.saveConfig()
        with open(RESOURCE_CONFIG, 'r') as config:
            temp = config.read()
        config = json.loads(temp)
        self.domain = config.get('domain', None)
        self.backupDestinationPaths = config.get('backupDestinationPaths', None)
        if self.domain is None or self.backupDestinationPaths is None:
            self.saveConfig()

    @ex_deco
    def domainChanged(self):
        self.domain = str(self.domainInput.textValue())
        print('[client] domainChanged. self.domain = %r ' % (self.domain,))
        self.saveConfig(self.domain, self.backupDestinationPaths)

    @ex_deco
    def pathChanged(self):
        path_str = str(self.pathInput.textValue())
        print('[client] pathChanged. path_str = %r ' % (path_str,))
        self.backupDestinationPaths = [ abspath(expanduser(path.strip())) for path in path_str.split(',') ]
        self.saveConfig(self.domain, self.backupDestinationPaths)

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
    def getImageDisplayFirstImage(self):
        return self.imageDisplay.first_image.current_image

    @ex_deco
    def getImageDisplayLastImage(self):
        return self.imageDisplay.last_image.current_image

    @ex_deco
    def getImageDisplayImageBoxes(self):
        return self.imageDisplay.image_boxes

    @ex_deco
    def setImageDisplayFirstImage(self, filename):
        self.imageDisplay.first_image.current_image = filename

    @ex_deco
    def setImageDisplayLastImage(self, filename):
        self.imageDisplay.last_image.current_image = filename

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
        print('[client] clear')
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
    # window.showMaximized()
    window.show()
    window.clear()
    sys.exit(app.exec_())
