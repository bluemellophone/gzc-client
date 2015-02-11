from PyQt4 import QtGui
from PyQt4 import QtCore
import sys
import image_import_client as iic
import gpsclient as gc
def main():
    
    app = QtGui.QApplication(sys.argv)
    tabs= QtGui.QTabWidget()
    
    # image_import tab
    MainWindow = QtGui.QMainWindow()
    ui = iic.image_import_interface(MainWindow)
    # ui.setupUi(MainWindow)
    tabs.addTab(ui, "Images")

    # GPS_import tab

    # QAPP = QtGui.QApplication(sys.argv)
    wgt = gc.GPSGuiWidget()
    wgt.show()
    # QAPP.setActiveWindow(wgt)
    # QAPP.exec_()
    tabs.addTab(wgt,"GPS")

    #Resize width and height
    tabs.resize(800, 600)
    
    #Move QTabWidget to x:300,y:300
    tabs.move(300, 300)
    
    tabs.setWindowTitle('\'The Great Zebra Count Image Upload\'')
    tabs.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()