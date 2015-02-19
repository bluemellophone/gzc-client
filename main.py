from PyQt4 import QtGui
from MainSkel import Ui_MainWindow
import sys
from widgets import sidebar as sb
from widgets import image_widgets as img


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.initWidgets()
        self.initConnect()

        self.setWindowTitle("Great Zebra Count 2015")
        # self.setStyleSheet("background-color: white;")

    def initWidgets(self):
        self.sidebar = sb.Sidebar(parent=self)
        self.sidebar.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        self.sidebar_space.addWidget(self.sidebar)
        self.current_display = 0 # 0 -> image display, 1 -> gps display
        self.img_display = img.selection_group()
        self.display_space.addWidget(self.img_display)

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
