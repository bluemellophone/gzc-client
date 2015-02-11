from PyQt4 import QtGui, QtCore
import sys
import platform

GPS_WIDGET_BASE = QtGui.QWidget
COLOR_BUTTON_BASE = QtGui.QPushButton


class colorSelectButton(COLOR_BUTTON_BASE):
    def __init__(self, text="", bgcolor=None, fgcolor=None, ischeckable=True):
        COLOR_BUTTON_BASE.__init__(self, text)
        self.setCheckable(ischeckable)
        style_sheet_str = self.make_style_sheet(bgcolor=bgcolor, fgcolor=fgcolor)
        if style_sheet_str is not None:
            self.setStyleSheet(style_sheet_str)

    def make_style_sheet(self, bgcolor=None, fgcolor=None):
        style_list = []
        fmtdict = {}
        if bgcolor is not None:
            style_list.append('background-color: rgb({bgcolor})')
            fmtdict['bgcolor'] = ','.join(map(str, bgcolor))
        if fgcolor is not None:
            style_list.append('color: rgb({fgcolor})')
            fmtdict['fgcolor'] = ','.join(map(str, fgcolor))
        style_list.append('padding-left: 0px')
        style_list.append('padding-right: 0px')
        if len(style_list) > 0:
            style_sheet_fmt = ';'.join(style_list)
            style_sheet_str = style_sheet_fmt.format(**fmtdict)
            return style_sheet_str
        else:
            return None


class GPSGuiWidget(GPS_WIDGET_BASE):
    def __init__(gpswgt, parent=None, flags=0):
        GPS_WIDGET_BASE.__init__(gpswgt)
        gpswgt.dpath = None
        gpswgt.buttonList = []
        gpswgt.map_image_file = "map.png"
        gpswgt._init_components()
        gpswgt._init_layout()
        gpswgt._init_signals()
        gpswgt.setWindowTitle(QtCore.QString("GPS Information Import"))

    def _init_components(gpswgt):
        # Layout Widgets
        gpswgt.pageLayout = QtGui.QVBoxLayout(gpswgt)

        # 0) Logo Widgets
        ibeisLogoImg = QtGui.QPixmap("ibeis_logo.png")
        gpswgt.ibeisLogoLabel = QtGui.QLabel()
        gpswgt.ibeisLogoLabel.setPixmap(ibeisLogoImg.scaled(50, 50))
        # 1) GPS CSV Select Widgets
        gpswgt.fileSelectLabel = QtGui.QLabel(QtCore.QString("1) Select GPS CSV file:"))
        gpswgt.fileSelectTextbox = QtGui.QLineEdit()
        gpswgt.browseButton = QtGui.QPushButton(QtCore.QString("Browse..."))

        # 2) Sync / Start Time Selection Widgets
        gpswgt.timeLabel = QtGui.QLabel(QtCore.QString("2) Select Car Start Time:"))
        gpswgt.timeEdit = QtGui.QTimeEdit()
        gpswgt.timeEdit.setDisplayFormat("h:mm AP")

        # 3) Import Button Widgets
        gpswgt.importLabel = QtGui.QLabel(QtCore.QString("3)"))
        gpswgt.importButton = QtGui.QPushButton(QtCore.QString("IMPORT"))
        # 4) Car Input Widgets
        gpswgt.carLabel = QtGui.QLabel(QtCore.QString("4) Select Car Color and Number:"))
        gpswgt.carNumberSelect = QtGui.QSpinBox()
        gpswgt.carNumberSelect.setMinimum(1)
        gpswgt.carNumberSelect.setMaximum(5000)

        colorList = ["Red", "Green", "Blue", "Yellow", "Black", "White", "Orange"]
        bgList = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 0, 0), (255, 255, 255), (255, 92, 0)]
        fgList = [(255, 255, 255), (255, 255, 255), (255, 255, 255), None, (255, 255, 255), None, None, None]

        gpswgt.carColor = QtGui.QButtonGroup(gpswgt)

        for color, bg, fg in zip(colorList, bgList, fgList):
            newButton = colorSelectButton(text=color, bgcolor=bg, fgcolor=fg)
            gpswgt.buttonList.append(newButton)
            gpswgt.carColor.addButton(newButton)

        #gpswgt.redButton = colorSelectButton(text="Red", bgcolor=(255, 0, 0), fgcolor=(255, 255, 255))
        #gpswgt.greenButton = colorSelectButton(text="Green", bgcolor=(0, 255, 0), fgcolor=(255, 255, 255))
        #gpswgt.blueButton = colorSelectButton(text="Blue", bgcolor=(0, 0, 255), fgcolor=(255, 255, 255))
        #gpswgt.yellowButton = colorSelectButton(text="Yellow", bgcolor=(255, 255, 0))
        #gpswgt.blackButton = colorSelectButton(text="Black", bgcolor=(0, 0, 0), fgcolor=(255, 255, 255))
        #gpswgt.whiteButton = colorSelectButton(text="White", bgcolor=(255, 255, 255))
        #gpswgt.orangeButton = colorSelectButton(text="Orange", bgcolor=(255, 92, 0))
        #gpswgt.carColor.addButton(gpswgt.redButton)
        #gpswgt.carColor.addButton(gpswgt.greenButton)
        #gpswgt.carColor.addButton(gpswgt.blueButton)
        #gpswgt.carColor.addButton(gpswgt.yellowButton)
        #gpswgt.carColor.addButton(gpswgt.blackButton)
        #gpswgt.carColor.addButton(gpswgt.whiteButton)
        #gpswgt.carColor.addButton(gpswgt.orangeButton)
        # 5) GPS Widgets
        gpsImg = QtGui.QPixmap(gpswgt.map_image_file)
        gpswgt.gpsImageLabel = QtGui.QLabel()
        gpswgt.gpsImageLabel.setPixmap(gpsImg.scaledToWidth(500))
        # 6) Status Area / Submit Button Widgets
        gpswgt.submitButton = colorSelectButton(text="Submit", bgcolor=(255, 255, 255), ischeckable=False)
        # 7) Reset Button Widgets
        gpswgt.resetButton = colorSelectButton(text="Reset", bgcolor=(255, 0, 0), ischeckable=False)

    def _init_layout(gpswgt):
        upperLayout = QtGui.QHBoxLayout()
        lowerLayout = QtGui.QHBoxLayout()
        leftBox = QtGui.QVBoxLayout()
        rightBox = QtGui.QVBoxLayout()
        # 0) Logo Widgets
        logoBox = QtGui.QHBoxLayout()
        logoBox.addWidget(gpswgt.ibeisLogoLabel)
        logoBox.addStretch()
        # 1) GPS CSV Select Widgets
        csvSelectBox = QtGui.QHBoxLayout()
        csvSelectBox.addWidget(gpswgt.fileSelectLabel)
        csvSelectBox.addWidget(gpswgt.fileSelectTextbox)
        csvSelectBox.addWidget(gpswgt.browseButton)
        csvSelectBox.addStretch()
        # 2) Sync / Start Time Selection Widgets
        timeBox = QtGui.QHBoxLayout()
        timeBox.addWidget(gpswgt.timeLabel)
        timeBox.addWidget(gpswgt.timeEdit)
        timeBox.addStretch()
        # 3) Import Button Widgets
        importBox = QtGui.QHBoxLayout()
        importBox.addWidget(gpswgt.importLabel)
        importBox.addWidget(gpswgt.importButton)
        importBox.addStretch()
        # 4) Car Input Widgets
        carBox = QtGui.QVBoxLayout()
        numberBox = QtGui.QHBoxLayout()
        colorBox = QtGui.QHBoxLayout()
        numberBox.addWidget(gpswgt.carLabel)
        numberBox.addWidget(gpswgt.carNumberSelect)
        numberBox.addStretch()

        for button in gpswgt.buttonList:
            colorBox.addWidget(button)
        colorBox.addStretch()
        #colorBox.addWidget(gpswgt.redButton)
        #colorBox.addWidget(gpswgt.greenButton)
        #colorBox.addWidget(gpswgt.blueButton)
        #colorBox.addWidget(gpswgt.yellowButton)
        #colorBox.addWidget(gpswgt.blackButton)
        #colorBox.addWidget(gpswgt.whiteButton)
        #colorBox.addWidget(gpswgt.orangeButton)

        carBox.addLayout(numberBox)
        carBox.addLayout(colorBox)

        # 5) GPS Widgets
        gpsBox = QtGui.QVBoxLayout()
        gpsBox.addWidget(gpswgt.gpsImageLabel)
        # 6) Status Area / Submit Button Widgets
        submitLayout = QtGui.QVBoxLayout()
        resetLayout = QtGui.QVBoxLayout()

        submitLayout.addWidget(gpswgt.submitButton)

        lowerLayout.addLayout(submitLayout)
        # 7) Reset Button Widgets
        resetLayout.addWidget(gpswgt.resetButton)
        lowerLayout.addLayout(resetLayout)

        # Layout Widgets
        leftBox.addLayout(logoBox)
        leftBox.addLayout(csvSelectBox)
        leftBox.addLayout(timeBox)
        leftBox.addLayout(importBox)
        leftBox.addLayout(carBox)
        leftBox.addStretch()

        #placeholderBox = QtGui.QHBoxLayout()

        #rightBox.addLayout(placeholderBox)
        rightBox.addLayout(gpsBox)
        rightBox.addStretch()

        upperLayout.addLayout(leftBox)
        upperLayout.addLayout(rightBox)

        gpswgt.pageLayout.addLayout(upperLayout)
        gpswgt.pageLayout.addLayout(lowerLayout)

    def _init_signals(gpswgt):
        gpswgt.browseButton.clicked.connect(gpswgt.open_directory)

    def open_directory(gpswgt):
        qdlg = QtGui.QFileDialog()
        # hack to fix the dialog window on ubuntu
        if 'ubuntu' in platform.platform().lower():
            qopt = QtGui.QFileDialog.ShowDirsOnly | QtGui.QFileDialog.DontUseNativeDialog
        else:
            qopt = QtGui.QFileDialog.ShowDirsOnly
        qtkw = {
            'options': qopt,
        }
        dpath = str(qdlg.getExistingDirectory(None, **qtkw))
        print('dpath = %r' % dpath)
        if dpath == '' or dpath is None:
            dpath = None
            gpswgt.dpath = dpath
            return dpath
        print('Selected Directory: %r' % dpath)
        gpswgt.dpath = dpath
        gpswgt.fileSelectTextbox.setText(QtCore.QString(dpath))

if __name__ == "__main__":
    QAPP = QtGui.QApplication(sys.argv)
    wgt = GPSGuiWidget()
    wgt.show()
    QAPP.setActiveWindow(wgt)
    QAPP.exec_()
