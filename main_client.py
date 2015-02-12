from PyQt4 import QtGui
from PyQt4 import QtCore
import sys
import image_import_client as iic
import gpsclient as gc

GZC_BASE_CLASS = QtGui.QMainWindow
#GZC_BASE_CLASS = QtGui.QWidget
#GZC_BASE_CLASS = QtGui.QTabWidget


class GZCMainWindow(GZC_BASE_CLASS):
    def __init__(gzc, parent=None):
        GZC_BASE_CLASS.__init__(gzc, parent)
        gzc.gps_client = gc.GPSGuiWidget(parent=gzc)
        gzc.image_client = iic.image_import_interface(gzc)
        gzc._init_widgets()
        gzc._init_tabs()
        gzc._init_status()
        gzc._init_layout()
        gzc.resize(1100, 600)

    def _init_widgets(gzc):
        gzc.tabs = QtGui.QTabWidget()
        gzc.status_bar = QtGui.QStatusBar()

    def _init_tabs(gzc):
        gzc.tabs.addTab(gzc.gps_client, "GPS")
        gzc.tabs.addTab(gzc.image_client, "Images")
        #gzc.addTab(gzc.gps_client, "GPS")
        #gzc.addTab(gzc.image_client, "Images")

    def _init_layout(gzc):
        gzc.setCentralWidget(gzc.tabs)
        #gzc.centralWidget = QtGui.QVBoxLayout(gzc)
        #gzc.centralWidget.addWidget(gzc.tabs)
        gzc.setSizePolicy(gzc.tabs.sizePolicy())
        gzc.gps_client.setSizePolicy(gzc.tabs.sizePolicy())
        gzc.image_client.setSizePolicy(gzc.tabs.sizePolicy())
        gzc.updateGeometry()

    def _init_status(gzc):
        gzc.setStatusBar(gzc.status_bar)
        gzc.status_bar.showMessage(QtCore.QString("Ready"))
        gzc.status_bar.setPalette(QtGui.QPalette(QtGui.QColor(255, 255, 255)))


def main():
    app = QtGui.QApplication(sys.argv)
    #tabs = QtGui.QTabWidget()

    MainWindow = GZCMainWindow()

    # image_import tab
    #MainWindow = QtGui.QMainWindow()
    #ui = iic.image_import_interface(MainWindow)
    # ui.setupUi(MainWindow)
    #tabs.addTab(ui, "Images")

    # GPS_import tab

    # QAPP = QtGui.QApplication(sys.argv)
    #wgt = gc.GPSGuiWidget()
    #wgt.show()
    ## QAPP.setActiveWindow(wgt)
    ## QAPP.exec_()
    #tabs.addTab(wgt, "GPS")
    ##MainWindow.addTab(wgt, "GPS")
    ##MainWindow.addTab(ui, "Images")

    ###Resize width and height
    #tabs.resize(800, 600)

    ##Move QTabWidget to x:300,y:300
    #tabs.move(300, 300)

    #tabs.setWindowTitle('\'The Great Zebra Count Image Upload\'')
    #tabs.show()
    MainWindow.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
