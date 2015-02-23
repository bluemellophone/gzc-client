from __future__ import absolute_import, division, print_function
from PyQt4 import QtGui, QtCore, QtWebKit
#import matplotlib.pyplot as plt
from clientfuncs import ImportThread
from os.path import join, exists  # NOQA


class gps_map(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        #self.map_image_file = '../assets/map_nairobi.png'
        #self.map_image_file = '../assets/map_albany.png'
        #self.map_image_file = '../assets/map_troy.png'
        self.map_image_file = '../assets/map_rpi.png'
        self.initComponents()
        self.initLayout()
        self.initSignals()

    def initComponents(self):
        # Layout Widgets
        self.pageLayout = QtGui.QVBoxLayout(self)
        gpsImg = QtGui.QPixmap(self.map_image_file)
        self.gpsImageLabel = QtGui.QLabel()
        self.gpsImageLabel.setScaledContents(True)
        self.gpsImageLabel.setPixmap(gpsImg)

        self.webView = QtWebKit.QWebView(self)
        self.gMapURL = self.parent.domain + '/map'
        self.webView.resize(1000, 500)
        self.webView.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Horizontal, QtCore.Qt.ScrollBarAlwaysOff)
        self.webView.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Vertical, QtCore.Qt.ScrollBarAlwaysOff)
        self.webView.setUrl(QtCore.QUrl(self.gMapURL))

    def initLayout(self):
        # self.pageLayout.addWidget(self.gpsImageLabel)
        self.pageLayout.addWidget(self.webView)

    def initSignals(self):
        self.worker_thread = ImportThread(self)
        self.worker_thread.finished.connect(self.drawTrack)

    def drawTrack(self):
        gpsImg = QtGui.QPixmap('figure.png')
        self.gpsImageLabel.setPixmap(gpsImg.scaled(self.gpsImageLabel.width(), self.gpsImageLabel.height(), aspectRatioMode=1))
        # self.parent.status_bar.setPalette(self.ready_palette)

    def clear(self):
        gpsImg = QtGui.QPixmap(self.map_image_file)
        self.gpsImageLabel.setPixmap(gpsImg)
