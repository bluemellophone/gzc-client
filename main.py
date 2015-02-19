from PyQt4 import QtGui
from MainSkel import Ui_MainWindow
import sys
from widgets import sidebar as sb
from widgets import image_widgets as img
from os.path import dirname, join



FILE_DPATH = dirname(__file__)
BUTTON_SIZE = 100
TOGGLE_BUTTON_CAM = join(FILE_DPATH, "/assets/icons/icon_camera.png")
TOGGLE_BUTTON_GPS = join(FILE_DPATH, "/assets/icons/icon_gps.png")

class QLabelButton(QtGui.QLabel):
    def __init(self, parent):
        QLabel.__init__(self, parent)

    def mouseReleaseEvent(self, ev):
        self.emit(SIGNAL('clicked()'))


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.initWidgets()
        self.initConnect()

        self.setWindowTitle("Great Zebra Count 2015")
        # self.setStyleSheet("background-color: white;")

        #self.toggle_button_cam_ic = QtGui.QPixmap(TOGGLE_BUTTON_CAM).scaled(BUTTON_SIZE, BUTTON_SIZE, QtCore.Qt.KeepAspectRatio)
        #self.toggle_button_gps_ic = QtGui.QPixmap(TOGGLE_BUTTON_GPS).scaled(BUTTON_SIZE, BUTTON_SIZE, QtCore.Qt.KeepAspectRatio)


    def initWidgets(self):
        self.sidebar = sb.Sidebar(parent=self)
        self.sidebar.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        self.sidebar_space.addWidget(self.sidebar)
        self.current_display = 0 # 0 -> image display, 1 -> gps display
        self.img_display = img.selection_group()
        self.display_space.addWidget(self.img_display)

        #self.toggle_button = QLabelButton()
        #self.toggle_button.setPixmap(self.toggle_button_cam_ic)
        #self.toggle_button.move(30, 30)

    def initConnect(self):
        self.toggle.released.connect(self.switchWidgets)
        #self.gps_tab.released.connect(self.gpsClicked)

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
    window.show()
    sys.exit(app.exec_())
