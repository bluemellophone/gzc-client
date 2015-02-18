from PyQt4 import QtCore, QtGui
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

    self.setStyleSheet("background-color: white;")

  def initWidgets(self):
    self.sidebar = sb.Sidebar()
    self.sidebar.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
    self.sidebar_space.addWidget(self.sidebar)
    self.img_display = img.selection_group()
    self.display_space.addWidget(self.img_display)

  def initConnect(self):
    self.image_tab.released.connect(self.imageClicked)
    self.gps_tab.released.connect(self.gpsClicked)

  def imageClicked(self):
    if self.image_tab.isChecked():
      self.gps_tab.setChecked(False)
      # do other switching to image stuff
      self.sidebar.switchWidgets()
    else:
      self.image_tab.setChecked(True)

  def gpsClicked(self):
    if self.gps_tab.isChecked():
      self.image_tab.setChecked(False)
      # do other switching to gps stuff
      self.sidebar.switchWidgets()
    else:
      self.gps_tab.setChecked(True)

  def switchFunction(self):
    self.sidebar.switchWidgets()



if __name__ == '__main__':
  app = QtGui.QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec_())
