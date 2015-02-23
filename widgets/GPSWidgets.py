from __future__ import absolute_import, division, print_function
from PyQt4 import QtGui
#import matplotlib.pyplot as plt
from clientfuncs import ImportThread
from os.path import join, exists  # NOQA


class gps_map(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        self.buttonList = []
        #self.map_image_file = "../assets/map_nairobi.png"
        #self.map_image_file = "../assets/map_albany.png"
        #self.map_image_file = "../assets/map_troy.png"
        self.map_image_file = "../assets/map_rpi.png"
        self.initComponents()
        self.initLayout()
        self.initSignals()
        self.processing_palette = QtGui.QPalette(QtGui.QColor(255, 255, 255))
        self.ready_palette = QtGui.QPalette(QtGui.QColor(155, 209, 229))
        self.sending_palette = QtGui.QPalette(QtGui.QColor(63, 124, 172))
        self.sent_palette = QtGui.QPalette(QtGui.QColor(0, 96, 6))
        self.error_palette = QtGui.QPalette(QtGui.QColor(163, 11, 55))

    def print_hello(self):
        print("Hello World")

    def initComponents(self):
        # Layout Widgets
        self.pageLayout = QtGui.QVBoxLayout(self)
        gpsImg = QtGui.QPixmap(self.map_image_file)
        self.gpsImageLabel = QtGui.QLabel()
        self.gpsImageLabel.setScaledContents(True)
        self.gpsImageLabel.setPixmap(gpsImg)

    def initLayout(self):
        self.pageLayout.addWidget(self.gpsImageLabel)

    def initSignals(self):
        self.worker_thread = ImportThread(self)
        self.worker_thread.finished.connect(self.drawTrack)

    def drawTrack(self):
        gpsImg = QtGui.QPixmap("figure.png")
        self.gpsImageLabel.setPixmap(gpsImg.scaled(self.gpsImageLabel.width(), self.gpsImageLabel.height(), aspectRatioMode=1))
        # self.parent.status_bar.setPalette(self.ready_palette)

    def clear(self):
        gpsImg = QtGui.QPixmap(self.map_image_file)
        self.gpsImageLabel.setPixmap(gpsImg)
