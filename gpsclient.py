from PyQt4 import QtGui, QtCore
import sys
#import platform
import import_gps_tracks
#import matplotlib.pyplot as plt
import numpy as np
from coordinate_map import CoordinateMap
import requests
import simplejson as json
from os.path import join, exists  # NOQA

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
        #style_list.append('padding-left: 0px')
        #style_list.append('padding-right: 0px')
        if len(style_list) > 0:
            style_sheet_fmt = ';'.join(style_list)
            style_sheet_str = style_sheet_fmt.format(**fmtdict)
            return style_sheet_str
        else:
            return None

    def change_color(self, bgcolor=None, fgcolor=None):
        style_list = []
        fmtdict = {}
        if bgcolor is not None:
            style_list.append('background-color: rgb({bgcolor})')
            fmtdict['bgcolor'] = ','.join(map(str, bgcolor))
        if fgcolor is not None:
            style_list.append('color: rgb({fgcolor})')
            fmtdict['fgcolor'] = ','.join(map(str, fgcolor))
        if len(style_list) > 0:
            style_sheet_fmt = ';'.join(style_list)
            style_sheet_str = style_sheet_fmt.format(**fmtdict)
        else:
            style_sheet_str = None
        if style_sheet_str is not None:
            self.setStyleSheet(style_sheet_str)


class GPSGuiWidget(GPS_WIDGET_BASE):
    def __init__(gpswgt, parent=None, flags=0):
        GPS_WIDGET_BASE.__init__(gpswgt)
        gpswgt.buttonList = []
        gpswgt.map_image_file = "map.png"
        #gpswgt.map_image_file = "troy_map.png"
        #gpswgt.map_image_file = "close_troy_map_small.png"
        #gpswgt.map_image_file = "rpi_map.png"
        gpswgt._init_components()
        gpswgt._init_layout()
        gpswgt._init_signals()
        gpswgt.setWindowTitle(QtCore.QString("GPS Information Import"))
        gpswgt.domain = "http://localhost:5000"

    def _init_components(gpswgt):
        # Layout Widgets
        gpswgt.pageLayout = QtGui.QVBoxLayout(gpswgt)

        # 0) Logo Widgets
        ibeisLogoImg = QtGui.QPixmap("ibeis_logo.png")
        gpswgt.ibeisLogoLabel = QtGui.QLabel()
        gpswgt.ibeisLogoLabel.setPixmap(ibeisLogoImg.scaled(100, 100))

        # 1) Car Input Widgets
        gpswgt.carLabel = QtGui.QLabel(QtCore.QString("1) Input Identification Info:"))
        gpswgt.numberLabel = QtGui.QLabel(QtCore.QString("Car Number:"))
        gpswgt.carNumberSelect = QtGui.QSpinBox()
        gpswgt.carNumberSelect.setMinimum(1)
        gpswgt.carNumberSelect.setMaximum(5000)

        # 2) Sync / Start Time Selection Widgets
        gpswgt.timeLabel = QtGui.QLabel(QtCore.QString("2) Select Car Start Time:"))
        gpswgt.timeEdit = QtGui.QTimeEdit()
        gpswgt.timeEdit.setDisplayFormat("h:mm AP")

        # 3) Import Button Widgets
        gpswgt.importLabel = QtGui.QLabel(QtCore.QString("3)"))
        gpswgt.importButton = QtGui.QPushButton(QtCore.QString("Import"))

        gpswgt.colorList = ["Red", "Green", "Blue", "Yellow", "Black", "White"]
        bgList = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 0, 0), (255, 255, 255)]
        fgList = [(255, 255, 255), (255, 255, 255), (255, 255, 255), None, (255, 255, 255), None, None]

        gpswgt.carColor = QtGui.QButtonGroup(gpswgt)

        for color, bg, fg in zip(gpswgt.colorList, bgList, fgList):
            newButton = colorSelectButton(text=color, bgcolor=bg, fgcolor=fg)
            gpswgt.buttonList.append(newButton)
            gpswgt.carColor.addButton(newButton)

        # 5) GPS Widgets
        gpsImg = QtGui.QPixmap(gpswgt.map_image_file)
        gpswgt.gpsImageLabel = QtGui.QLabel()
        gpswgt.gpsImageLabel.setPixmap(gpsImg)
        # 6) Status Area / Submit Button Widgets
        gpswgt.submitButton = colorSelectButton(text="Submit", bgcolor=(255, 255, 255), ischeckable=False)
        # 7) Reset Button Widgets
        gpswgt.resetButton = colorSelectButton(text="Reset", bgcolor=(205, 201, 201), ischeckable=False)

    def _init_layout(gpswgt):
        upperLayout = QtGui.QHBoxLayout()
        lowerLayout = QtGui.QHBoxLayout()
        leftBox = QtGui.QVBoxLayout()
        rightBox = QtGui.QVBoxLayout()
        # 0) Logo Widgets
        logoBox = QtGui.QHBoxLayout()
        logoBox.addWidget(gpswgt.ibeisLogoLabel)
        logoBox.addStretch()
        # 1) Car Input Widgets
        carBox = QtGui.QVBoxLayout()
        numberBox = QtGui.QHBoxLayout()
        colorBoxTop = QtGui.QHBoxLayout()
        colorBoxBottom = QtGui.QHBoxLayout()
        numberBox.addWidget(gpswgt.carLabel)
        numberBox.addStretch()

        for button in gpswgt.buttonList[:len(gpswgt.buttonList) / 2]:
            colorBoxTop.addWidget(button)
        for button in gpswgt.buttonList[len(gpswgt.buttonList) / 2:]:
            colorBoxBottom.addWidget(button)
        colorBoxTop.addWidget(gpswgt.numberLabel)
        colorBoxTop.addWidget(gpswgt.carNumberSelect)
        colorBoxTop.addStretch()
        colorBoxBottom.addStretch()
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

        carBox.addLayout(numberBox)
        carBox.addLayout(colorBoxTop)
        carBox.addLayout(colorBoxBottom)

        # 5) GPS Widgets
        gpsBox = QtGui.QVBoxLayout()
        gpsBox.addWidget(gpswgt.gpsImageLabel)
        # 6) Status Area / Submit Button Widgets
        submitLayout = QtGui.QVBoxLayout()
        resetLayout = QtGui.QVBoxLayout()

        submitLayout.addWidget(gpswgt.submitButton)

        lowerLayout.addStretch()
        lowerLayout.addLayout(submitLayout)
        # 7) Reset Button Widgets
        resetLayout.addWidget(gpswgt.resetButton)
        lowerLayout.addLayout(resetLayout)

        # Layout Widgets
        leftBox.addLayout(logoBox)
        leftBox.addLayout(carBox)
        leftBox.addLayout(timeBox)
        leftBox.addLayout(importBox)
        leftBox.addStretch()

        rightBox.addLayout(gpsBox)
        rightBox.addStretch()

        upperLayout.addLayout(leftBox)
        upperLayout.addLayout(rightBox)

        gpswgt.pageLayout.addLayout(upperLayout)
        gpswgt.pageLayout.addLayout(lowerLayout)

    def _init_signals(gpswgt):
        gpswgt.importButton.clicked.connect(gpswgt._import_gpx)
        gpswgt.submitButton.clicked.connect(gpswgt._submit_gps)
        gpswgt.resetButton.clicked.connect(gpswgt._reset_interface)

    def compile_data(gpswgt):
        color_index = gpswgt.carColor.checkedId()
        if color_index == -1:
            print("Error: No Car Color Selected")
            return None
        car_color = gpswgt.colorList[abs(color_index) - 2]
        car_number = gpswgt.carNumberSelect.value()
        gps_start_time = gpswgt.timeEdit.time()
        gps_start_time_hour = gps_start_time.hour()
        gps_start_time_minute = gps_start_time.minute()
        data = {
            'car_color': car_color,
            'car_number': car_number,
            'gps_start_time_hour': gps_start_time_hour,
            'gps_start_time_minute': gps_start_time_minute,
        }
        return data

    def _import_gpx(gpswgt):
        #When hooked up to a i-gotu gps dongle
        data = gpswgt.compile_data()
        if(data is None):
            print("Must select a color first")
            gpswgt.submitButton.change_color(bgcolor=(163, 11, 55))
            return
        try:
            gpx_string = import_gps_tracks.import_gpx(data)
        except IOError:
            print("Could not import GPX file")
            return
        #from mpl_toolkits.basemap import Basemap
        import cv2
        #gpx_string = open("test_gps/track.gpx", "r").read()
        gps_json = import_gps_tracks.convert_gpx_to_json(gpx_string)
        if len(gps_json['track']) == 0:
            print("No points found")
            gpswgt.submitButton.change_color(bgcolor=(163, 11, 55))
            return
        lats = []
        lons = []
        xs = []
        ys = []
        pts = []
        img = cv2.imread(gpswgt.map_image_file)
        coord_map = CoordinateMap((-1.32504, 36.766777), (-1.442833, 36.965561), img)  # Nairobi (map.png)
        #coord_map = CoordinateMap((42.789920, -73.759957), (42.673663, -73.592416), img)  # Troy (troy_map.png)
        #coord_map = CoordinateMap((42.740739, -73.697043), (42.720154, -73.657561), img)  # Close up Troy (close_troy_map_small.png)
        #coord_map = CoordinateMap((42.735759, -73.686637), (42.726444, -73.664621), img)  # RPI Campus (rpi_map.png)
        for point in gps_json['track']:
            lat = point['lat']
            lon = point['lon']
            lats.append(lat)
            lons.append(lon)
            x, y = coord_map.map_point_float((lat, lon))
            pts.append(np.array([x, y]))
            xs.append(x)
            ys.append(y)

        lats = np.array(lats)
        lons = np.array(lons)

        cv2.polylines(img, [np.array(pts, dtype=np.int32)], False, (255, 0, 0), thickness=2)
        cv2.imwrite("figure.png", img)
        gpsImg = QtGui.QPixmap("figure.png")
        gpswgt.gpsImageLabel.setPixmap(gpsImg.scaled(gpswgt.gpsImageLabel.width(), gpswgt.gpsImageLabel.height(), aspectRatioMode=1))
        gpswgt.submitButton.change_color(bgcolor=(155, 209, 229))

    def _submit_gps(gpswgt):
        gpswgt.submitButton.change_color(bgcolor=(63, 124, 172))
        data = gpswgt.compile_data()

        GPSURL = gpswgt.domain + '/gps/submit'
        DEFAULT_DATA_DIR = 'data'

        # Process gps for car
        try:
            car_color  = data['car_color'].lower()
        except TypeError:
            print("Must select a color first")
            gpswgt.submitButton.change_color(bgcolor=(163, 11, 55))
            return
        car_number = str(data['car_number'])
        # Ensure the folder
        car_dir = import_gps_tracks.ensure_structure(DEFAULT_DATA_DIR, 'gps', car_number, car_color)
        gps_path  = join(car_dir, 'track.gpx')

        # gps data
        try:
            content = open(join(gps_path), 'rb')
        except IOError:
            print("No file exists. Import first.")
            gpswgt.submitButton.change_color(bgcolor=(163, 11, 55))
            return
        files = {
            'gps_data': content,
        }

        r = requests.post(GPSURL, data=data, files=files)
        print("HTTP STATUS:", r.status_code)
        try:
            response = json.loads(r.text)
            print("RESPONSE:", response)
        except json.scanner.JSONDecodeError:
            print("JSON file not readable. Import again")
        if r.status_code == 200:
            gpswgt.submitButton.change_color(bgcolor=(0, 96, 6))
        else:
            gpswgt.submitButton.change_color(bgcolor=(163, 11, 55))
        return r.status_code

    def _reset_interface(gpswgt):
        gpsImg = QtGui.QPixmap(gpswgt.map_image_file)
        gpswgt.gpsImageLabel.setPixmap(gpsImg)

        gpswgt.timeEdit.setTime(gpswgt.timeEdit.minimumTime())
        gpswgt.carNumberSelect.setValue(gpswgt.carNumberSelect.minimum())

        color_index = gpswgt.carColor.checkedId()
        if color_index != -1:
            checked_button = gpswgt.buttonList[abs(color_index) - 2]
            checked_button.setChecked(False)

        gpswgt.submitButton.change_color(bgcolor=(255, 255, 255))


if __name__ == "__main__":
    QAPP = QtGui.QApplication(sys.argv)
    wgt = GPSGuiWidget()
    wgt.show()
    QAPP.setActiveWindow(wgt)
    QAPP.exec_()
