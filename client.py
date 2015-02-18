#!/usr/bin/env python
from __future__ import absolute_import, division, print_function
from PyQt4 import QtGui
from PyQt4 import QtCore
import sys
import client_image as iic
import client_gps as gc

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
        gzc._init_signals()
        gzc._init_menus()
        gzc.domain = "http://localhost:5000"

    def _init_widgets(gzc):
        gzc.tabs = QtGui.QTabWidget()
        gzc.status_bar = QtGui.QStatusBar()

        gzc.menu_bar = QtGui.QMenuBar()

        gzc.options_menu = QtGui.QMenu()
        gzc.options_menu.setTitle("Options")
        gzc.options_menu.addAction("Set Domain")

        gzc.domain_dialog = QtGui.QInputDialog()
        gzc.domain_dialog.setLabelText(QtCore.QString("Enter server domain:"))

    def _init_tabs(gzc):
        gzc.tabs.addTab(gzc.image_client, "Images")
        gzc.tabs.addTab(gzc.gps_client, "GPS")
        #gzc.addTab(gzc.gps_client, "GPS")
        #gzc.addTab(gzc.image_client, "Images")

    def _init_layout(gzc):
        gzc.setCentralWidget(gzc.tabs)
        gzc.setWindowTitle("The Great Zebra Count")
        #gzc.centralWidget = QtGui.QVBoxLayout(gzc)
        #gzc.centralWidget.addWidget(gzc.tabs)
        #gzc.setSizePolicy(gzc.tabs.sizePolicy())
        #gzc.gps_client.setSizePolicy(gzc.tabs.sizePolicy())
        #gzc.image_client.setSizePolicy(gzc.tabs.sizePolicy())
        #gzc.updateGeometry()

    def _init_status(gzc):
        gzc.setStatusBar(gzc.status_bar)
        gzc.status_bar.showMessage(QtCore.QString("Ready"))
        gzc.status_bar.setPalette(QtGui.QPalette(QtGui.QColor(255, 255, 255)))

    def _init_signals(gzc):
        gzc.options_menu.triggered.connect(gzc.options_clicked)
        gzc.domain_dialog.accepted.connect(gzc.change_domain)

    def _init_menus(gzc):
        gzc.menu_bar.addMenu(gzc.options_menu)
        gzc.setMenuBar(gzc.menu_bar)

    def options_clicked(gzc, action):
        if str(action.text()) == "Set Domain":
            gzc.set_domain()
        else:
            print("Not correct")

    def set_domain(gzc):
        gzc.domain_dialog.setTextValue(gzc.domain)
        gzc.domain_dialog.show()

    def change_domain(gzc):
        gzc.domain = str(gzc.domain_dialog.textValue())


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
