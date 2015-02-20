#!/usr/bin/env python
from PyQt4 import QtGui, QtCore
from MainSkel import Ui_MainWindow
import sys
import signal
from widgets import sidebar as sb
from widgets import image_widgets as img
from os.path import dirname, join


FILE_DPATH = dirname(__file__)
BUTTON_SIZE = 100
TOGGLE_BUTTON_CAM = join(FILE_DPATH, "assets/icons/icon_camera.png")
TOGGLE_BUTTON_GPS = join(FILE_DPATH, "assets/icons/icon_gps.png")


class QLabelButton(QtGui.QLabel):
    clicked = QtCore.pyqtSignal(name="toggle_clicked")

    def __init__(self, icon1=None, icon2=None):
        QtGui.QLabel.__init__(self)
        self.icon1 = icon1
        self.icon2 = icon2
        self.setPixmap(icon1)
        self.current = 0

    def mouseReleaseEvent(self, ev):
        if ev.button() == QtCore.Qt.LeftButton and ev.x() >= ev.y():
            self.current = (self.current + 1) % 2
            if self.current == 0:
                self.setPixmap(self.icon1)
            else:
                self.setPixmap(self.icon2)
            self.clicked.emit()


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.toggle_button_cam_ic = QtGui.QPixmap(TOGGLE_BUTTON_CAM).scaled(BUTTON_SIZE, BUTTON_SIZE, QtCore.Qt.KeepAspectRatio)
        self.toggle_button_gps_ic = QtGui.QPixmap(TOGGLE_BUTTON_GPS).scaled(BUTTON_SIZE, BUTTON_SIZE, QtCore.Qt.KeepAspectRatio)
        self.initWidgets()
        self.initConnect()

        self.setWindowTitle("Great Zebra Count 2015")
        # self.setStyleSheet("background-color: white;")

    def resizeEvent(self, ev):
        self.toggle_button.move(self.width() - self.toggle_button.width(), 0)


    def initWidgets(self):
        self.sidebar = sb.Sidebar(parent=self)
        self.sidebar.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        self.sidebar_space.addWidget(self.sidebar)
        self.current_display = 0  # 0 -> image display, 1 -> gps display
        self.img_display = img.selection_group()
        self.display_space.addWidget(self.img_display)

        self.toggle_button = QLabelButton(icon1=self.toggle_button_cam_ic, icon2=self.toggle_button_gps_ic)
        self.toggle_button.resize(100, 100)
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
