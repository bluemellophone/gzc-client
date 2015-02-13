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
from QwwColorComboBox import QwwColorComboBox

GPS_WIDGET_BASE = QtGui.QWidget
COLOR_BUTTON_BASE = QtGui.QPushButton


class ImportThread(QtCore.QThread):
    def __init__(thrd, gpswgt):
        QtCore.QThread.__init__(thrd)
        thrd.gpswgt = gpswgt

    def run(thrd):
        #When hooked up to a i-gotu gps dongle
        data = thrd.gpswgt.compile_data()
        thrd.gpswgt.parent.status_bar.showMessage(QtCore.QString("Importing GPS information"))
        try:
            gpx_string = import_gps_tracks.import_gpx(data)
        except IOError:
            thrd.gpswgt.parent.status_bar.showMessage(QtCore.QString("Couldn't import GPS info. Make sure the dongle is connected"))
            thrd.gpswgt.parent.status_bar.setPalette(thrd.gpswgt.error_palette)
            return
        import cv2
        #gpx_string = open("test_gps/track.gpx", "r").read()
        ## Process gps for car
        #car_color  = data['car_color'].lower()
        #car_number = str(data['car_number'])
        ## Ensure the folder
        #car_dir = import_gps_tracks.ensure_structure('data', 'gps', car_number, car_color)
        #gps_path  = join(car_dir, 'track.gpx')
        #f = open(gps_path, 'w')
        #f.write(gpx_string)
        #f.close()
        gps_json = import_gps_tracks.convert_gpx_to_json(gpx_string)
        if len(gps_json['track']) == 0:
            thrd.gpswgt.parent.status_bar.showMessage(QtCore.QString("No Points found. Import again."))
            thrd.gpswgt.parent.status_bar.setPalette(thrd.gpswgt.error_palette)
            return
        pts = []
        img = cv2.imread(thrd.gpswgt.map_image_file)
        #coord_map = CoordinateMap((-1.32504, 36.766777), (-1.442833, 36.965561), img)  # Nairobi (map.png)
        #coord_map = CoordinateMap((42.789920, -73.759957), (42.673663, -73.592416), img)  # Troy (troy_map.png)
        #coord_map = CoordinateMap((42.740739, -73.697043), (42.720154, -73.657561), img)  # Close up Troy (close_troy_map_small.png)
        coord_map = CoordinateMap((42.735759, -73.686637), (42.726444, -73.664621), img)  # RPI Campus (rpi_map.png)
        for point in gps_json['track']:
            lat = point['lat']
            lon = point['lon']
            x, y = coord_map.map_point_float((lat, lon))
            pts.append(np.array([x, y]))

        cv2.polylines(img, [np.array(pts, dtype=np.int32)], False, (255, 0, 0), thickness=2)
        cv2.imwrite("figure.png", img)

    def begin(thrd):
        thrd.start()


class GPSGuiWidget(GPS_WIDGET_BASE):
    def __init__(gpswgt, parent=None, flags=0):
        GPS_WIDGET_BASE.__init__(gpswgt)
        gpswgt.parent = parent
        gpswgt.buttonList = []
        #gpswgt.map_image_file = "map.png"
        #gpswgt.map_image_file = "troy_map.png"
        #gpswgt.map_image_file = "close_troy_map_small.png"
        gpswgt.map_image_file = "rpi_map.png"
        gpswgt._init_components()
        gpswgt._init_layout()
        gpswgt._init_signals()
        gpswgt.setWindowTitle(QtCore.QString("GPS Information Import"))
        gpswgt.processing_palette = QtGui.QPalette(QtGui.QColor(255, 255, 255))
        gpswgt.ready_palette = QtGui.QPalette(QtGui.QColor(155, 209, 229))
        gpswgt.sending_palette = QtGui.QPalette(QtGui.QColor(63, 124, 172))
        gpswgt.sent_palette = QtGui.QPalette(QtGui.QColor(0, 96, 6))
        gpswgt.error_palette = QtGui.QPalette(QtGui.QColor(163, 11, 55))

    def print_hello(gpswgt):
        print("Hello World")

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
        gpswgt.colorBox = QwwColorComboBox()
        for color_name, rgb in zip(gpswgt.colorList, bgList):
            color = QtGui.QColor(rgb[0], rgb[1], rgb[2])
            gpswgt.colorBox.addColor(color, color_name)

        # 5) GPS Widgets
        gpsImg = QtGui.QPixmap(gpswgt.map_image_file)
        gpswgt.gpsImageLabel = QtGui.QLabel()
        gpswgt.gpsImageLabel.setPixmap(gpsImg)
        # 6) Status Area / Submit Button Widgets
        gpswgt.submitButton = QtGui.QPushButton("Submit")
        # 7) Reset Button Widgets
        gpswgt.resetButton = QtGui.QPushButton("Reset")

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
        numberBox.addWidget(gpswgt.carLabel)
        numberBox.addStretch()

        colorBoxTop.addWidget(gpswgt.colorBox)
        colorBoxTop.addWidget(gpswgt.carNumberSelect)
        colorBoxTop.addStretch()
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
        #carBox.addLayout(colorBoxBottom)

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
        gpswgt.pageLayout.addStretch()

    def _init_signals(gpswgt):
        gpswgt.worker_thread = ImportThread(gpswgt)
        gpswgt.importButton.clicked.connect(gpswgt.worker_thread.begin)
        gpswgt.submitButton.clicked.connect(gpswgt._submit_gps)
        gpswgt.resetButton.clicked.connect(gpswgt._reset_interface)
        gpswgt.worker_thread.finished.connect(gpswgt._draw_image)

    def compile_data(gpswgt):
        car_color = str(gpswgt.colorBox.currentText())
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

    def _draw_image(gpswgt):
        gpsImg = QtGui.QPixmap("figure.png")
        gpswgt.gpsImageLabel.setPixmap(gpsImg.scaled(gpswgt.gpsImageLabel.width(), gpswgt.gpsImageLabel.height(), aspectRatioMode=1))
        gpswgt.parent.status_bar.setPalette(gpswgt.ready_palette)

    def _submit_gps(gpswgt):
        gpswgt.parent.status_bar.showMessage("Submitting to server")
        gpswgt.parent.status_bar.setPalette(gpswgt.sending_palette)
        data = gpswgt.compile_data()

        GPSURL = gpswgt.parent.domain + '/gps/submit'
        DEFAULT_DATA_DIR = 'data'

        # Process gps for car
        car_color  = data['car_color'].lower()
        car_number = str(data['car_number'])
        # Ensure the folder
        car_dir = import_gps_tracks.ensure_structure(DEFAULT_DATA_DIR, 'gps', car_number, car_color)
        gps_path  = join(car_dir, 'track.gpx')

        # gps data
        try:
            content = open(join(gps_path), 'rb')
        except IOError:
            gpswgt.parent.status_bar.showMessage(QtCore.QString("No file exists. Import first."))
            gpswgt.parent.status_bar.setPalette(gpswgt.error_palette)
            return
        files = {
            'gps_data': content,
        }

        try:
            r = requests.post(GPSURL, data=data, files=files)
        except requests.exceptions.ConnectionError:
            gpswgt.parent.status_bar.showMessage(QtCore.QString("Couldn't connect to server. Ensure that the server is running and the domain is correct."))
            gpswgt.parent.status_bar.setPalette(gpswgt.error_palette)
            return
        print("HTTP STATUS:", r.status_code)
        response = json.loads(r.text)
        print("RESPONSE:", response)
        if r.status_code == 200:
            gpswgt.parent.status_bar.showMessage(QtCore.QString("Submit successful."))
            gpswgt.parent.status_bar.setPalette(gpswgt.sent_palette)
        else:
            gpswgt.parent.status_bar.showMessage(QtCore.QString("Submit failed. Error %r" % r.status_code))
            gpswgt.parent.status_bar.setPalette(gpswgt.error_palette)
        return r.status_code

    def _reset_interface(gpswgt):
        gpsImg = QtGui.QPixmap(gpswgt.map_image_file)
        gpswgt.gpsImageLabel.setPixmap(gpsImg)

        gpswgt.timeEdit.setTime(gpswgt.timeEdit.minimumTime())
        gpswgt.carNumberSelect.setValue(gpswgt.carNumberSelect.minimum())

        gpswgt.parent.status_bar.setPalette(gpswgt.processing_palette)
        gpswgt.parent.status_bar.showMessage(QtCore.QString("Ready"))


if __name__ == "__main__":
    QAPP = QtGui.QApplication(sys.argv)
    wgt = GPSGuiWidget()
    wgt.show()
    QAPP.setActiveWindow(wgt)
    QAPP.exec_()
