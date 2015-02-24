import sys
from PyQt4 import QtCore, QtGui
from SidebarSkel import Ui_Sidebar
from ImageFormSkel import Ui_ImageForm
from GPSFormSkel import Ui_GPSForm
from GZCQWidgets import QwwColorComboBox
from os.path import join, basename, exists, abspath
from shutil import rmtree
from clientfuncs import CopyThread, find_candidates, ex_deco, ensure_structure
import zipfile
import random
import simplejson as json
import requests


LOGO_SIZE     = 200
LOGO          = abspath('assets/logo_ibeis_alpha.png')
# LOGO          = abspath('assets/logo_kwf_alpha.png')
# LOGO          = abspath('assets/logo_kws_alpha.png')
IMPORT_ICON   = abspath('assets/icons/icon_import.png')
BROWSE_ICON   = abspath('assets/icons/icon_browse.png')
CLEAR_ICON    = abspath('assets/icons/icon_trash.png')
SUBMIT_ICON   = abspath('assets/icons/icon_upload.png')
ACCEPTED_ICON = abspath('assets/icons/icon_accepted.png')
REJECTED_ICON = abspath('assets/icons/icon_rejected.png')

CAR_COLORS = [('Select Color', '#F6F6F6')] + [
    ('white',    '#FFFFFF'),
    ('red',        '#D9534F'),
    ('orange', '#EF7A4C'),
    ('yellow', '#F0AD4E'),
    ('green',    '#5CB85C'),
    ('blue',     '#3071A9'),
    ('purple', '#6F5499'),
    ('black',    '#333333'),
]
CAR_NUMBER = ['Select Number'] + map(str, range(1, 26))  # 51
PERSON_LETTERS = ['Select Letter'] + ['a', 'b', 'c', 'd', 'e', 'f']  # , 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'aa', 'bb', 'cc', 'dd', 'ee', 'ff', 'gg', 'hh', 'ii', 'jj', 'kk', 'll', 'mm', 'nn', 'oo', 'pp', 'qq', 'rr', 'ss', 'tt', 'uu', 'vv', 'ww', 'xx', 'yy', 'zz']
TIME_HOUR_RANGE = range(6, 23)


class Sidebar(QtGui.QWidget, Ui_Sidebar):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self)
        self.parent = parent
        self.copyThread = None
        self.setupUi(self)
        self.initWidgets()
        self.initConnect()
        self.initVisuals()

    def initWidgets(self):
        # Load Image Form
        self.imageForm = ImageForm(self)
        self.form.addWidget(self.imageForm)
        # Load GPS Form
        self.gpsForm = GPSForm(self)
        self.form.addWidget(self.gpsForm)
        # Load logos
        self.initLogos()
        self.parent.clearGPSDisplay()

    def initLogos(self):
        logo = QtGui.QPixmap(LOGO).scaled(QtCore.QSize(LOGO_SIZE, LOGO_SIZE), QtCore.Qt.KeepAspectRatio, 1)
        self.logo.setPixmap(logo)

    def initConnect(self):
        self.submitButton.clicked.connect(self.submitClicked)
        self.clearButton.clicked.connect(self.clearClicked)
        self.connect(self.parent.imageDisplay, QtCore.SIGNAL('images_modified'), self.updateStatus)

    def initVisuals(self):
        # Setup clear icon
        self.clearButton.setText('')
        self.clearButton.setIcon(QtGui.QIcon(CLEAR_ICON))
        # Clear Sidebar
        self.clear()

    # Slots
    @ex_deco
    def submitClicked(self, *args):
        if self.parent.currentDisplay == 0:
            if self.complete_image_step_5:
                self.submitImage()
            else:
                self.copyImage()
        elif self.parent.currentDisplay == 1:
            if self.complete_gps_step_3:
                self.submitGPS()
            else:
                self.copyGPS()

    def clearClicked(self):
        self.clear()

    # Functions
    def updateStatus(self):
        if self.parent.currentDisplay == 0:
            # Image - Step 0 (always show)
            self.imageForm.driveLayout.show()
            self.imageForm.nameInput.setEnabled(True)
            # Image - Step 1
            if self.complete_image_step_1:
                self.imageForm.idLayout.show()
            else:
                self.imageForm.idLayout.hide()
            # Image - Step 2
            if self.complete_image_step_2:
                if self.import_directory == "overridden":
                    self.imageForm.nameInput.setEnabled(False)
                    self.imageForm.nameInput.setText(basename(self.image_file_list[0]))
                    self.complete_image_step_3_name = True
                self.imageForm.syncLayout.show()
            else:
                self.imageForm.syncLayout.hide()
            # Image - Step 3
            if self.complete_image_step_3_name and self.complete_image_step_3_time:
                self.submitButton.setEnabled(True)
            else:
                self.submitButton.setEnabled(False)
            # Image - Step 4 (Import)
            if self.complete_image_step_4:
                self.complete_image_step_5 = self.parent.allImagesSelected()
            else:
                self.complete_image_step_5 = False
            # Image - Step 5 (Images)
            if self.complete_image_step_5:
                self.submitButton.setIcon(QtGui.QIcon(SUBMIT_ICON))
                self.submitButton.setText('Submit')
            else:
                self.submitButton.setIcon(QtGui.QIcon(IMPORT_ICON))
                self.submitButton.setText('Import Card')
            # Image - Step 6 (Submit)
            if self.complete_image_step_6 is not None:
                if self.complete_image_step_6:
                    self.submitButton.setIcon(QtGui.QIcon(ACCEPTED_ICON))
                    self.submitButton.setText('Images Accepted')
                else:
                    self.submitButton.setIcon(QtGui.QIcon(REJECTED_ICON))
                    self.submitButton.setText('Images Rejected')
        elif self.parent.currentDisplay == 1:
            # GPS - Step 0 (always show)
            self.gpsForm.idLayout.show()
            # GPS - Step 1 (Car Information)
            if self.complete_gps_step_1:
                self.gpsForm.syncLayout.show()
            else:
                self.gpsForm.syncLayout.hide()
            # GPS - Step 2 (Sync Information)
            if self.complete_gps_step_2:
                self.submitButton.setEnabled(True)
            else:
                self.submitButton.setEnabled(False)
            # GPS - Step 3 (Importing/Submitting)
            if self.complete_gps_step_3:
                self.submitButton.setIcon(QtGui.QIcon(SUBMIT_ICON))
                self.submitButton.setText('Submit')
            else:
                self.submitButton.setIcon(QtGui.QIcon(IMPORT_ICON))
                self.submitButton.setText('Import Track')
            # Image - Step 4 (Submit)
            if self.complete_gps_step_4 is not None:
                if self.complete_gps_step_4:
                    self.submitButton.setIcon(QtGui.QIcon(ACCEPTED_ICON))
                    self.submitButton.setText('Track Accepted')
                else:
                    self.submitButton.setIcon(QtGui.QIcon(REJECTED_ICON))
                    self.submitButton.setText('Track Rejected')

    def move_file_list(self, file_list):
        self.parent.imageDisplay.first_image.current_image = file_list.pop(0)
        self.parent.imageDisplay.last_image.current_image = file_list.pop()
        # self.image_selection_group.stored_files = file_list

    def update_recent_file_image(self, index, filename):
        self.sidebarStatus.setText('Copying %s / %s' % (index + 1, len(self.image_file_list), ))
        add_to_display = index in self.image_file_list_random_indices
        self.parent.imageDisplay.add_filename(filename, add_to_display=add_to_display)

    def update_recent_file_gps(self, index, filename):
        self.sidebarStatus.setText('Copying GPX file...')

    def reset_cursor(self):
        QtGui.QApplication.restoreOverrideCursor()
        self.sidebarStatus.setText('Copying completed')
        if self.parent.currentDisplay == 0 and len(self.image_file_list) > 0:
            self.complete_image_step_4 = True
        elif self.parent.currentDisplay == 1:
            self.complete_gps_step_3 = True
        self.updateStatus()

    @ex_deco
    def copyImage(self):
        # Change cursor to busy
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        # Clear imageDisplay
        self.parent.clearImageDisplay()
        # Get information from form
        car_number    = str(self.imageForm.numberInput.currentText())
        car_color     = str(self.imageForm.colorInput.currentText())
        person_letter = str(self.imageForm.letterInput.currentText())
        # print('IMPORT SELF %r' % (self,))
        #print('IMPORT ARGS %r' % (args,))
        directory = self.import_directory
        # print (directory)
        if directory is None or directory == '':
            self.reset_cursor()
            raise IOError('Please select the directory that contains the photos you wish to import from.')
            return
        if str(self.imageForm.nameInput.text()) == '':
            self.reset_cursor()
            raise IOError('The first image name must be defined.')
            return
        if directory != "overridden":
            self.image_file_list = find_candidates(directory, str(self.imageForm.nameInput.text()))
            # Create random indices
            self.image_file_list_random_indices = set()
            while len(self.image_file_list_random_indices) < min(10, len(self.image_file_list)):
                rand_index = random.randint(0, len(self.image_file_list) - 1)
                self.image_file_list_random_indices.add(rand_index)
        if len(self.image_file_list) == 0:
            self.reset_cursor()
            raise IOError('Could not find any files for selected directory. Please check your first image name.')
            return
        #send this file list to the selection group i am a bad programmer
        self.file_bases = [basename(f) for f in self.image_file_list]
        # print self.file_bases
        self.move_file_list(self.file_bases)

        for index, path in enumerate(self.parent.path_list):
            dst_directory = ensure_structure(path, 'images', car_number, car_color, person_letter)
            if exists(dst_directory):
                print('Target directory already exists... deleting')
                rmtree(dst_directory)
            self.copyThread = CopyThread(self.image_file_list, [dst_directory])
            if index == 0:
                self.connect(self.copyThread, QtCore.SIGNAL('file_done'), self.update_recent_file_image)
                self.connect(self.copyThread, QtCore.SIGNAL('completed'), self.reset_cursor)
            self.copyThread.start()

    @ex_deco
    def copyGPS(self, pre_extracted_gpx_path=None):
        # Change cursor to busy
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.sidebarStatus.setText('Copying GPS Track')

        # Assert filled out
        color_index  = self.gpsForm.colorInput.currentIndex()
        number_index = self.gpsForm.numberInput.currentIndex()
        if color_index == 0 or number_index == 0:
            raise ValueError('Cannot import GPX file without specifying a car color and car number')

        # Get data from form
        car_number    = str(self.gpsForm.numberInput.currentText())
        car_color     = str(self.gpsForm.colorInput.currentText())

        for index, path in enumerate(self.parent.path_list):
            dst_directory = ensure_structure(path, 'gps', car_number, car_color)
            if exists(dst_directory):
                print('Target directory already exists... deleting')
                rmtree(dst_directory)
            if pre_extracted_gpx_path is not None:
                self.gps_file_list.append(pre_extracted_gpx_path)
                with open(pre_extracted_gpx_path) as gpx_file:
                    gpx_track = gpx_file.read()
                    self.parent.displayGPXTrack(gpx_track)
            else:
                print('call igotu2gpx', dst_directory)
            self.copyThread = CopyThread(self.gps_file_list, [dst_directory])
            if index == 0:
                self.connect(self.copyThread, QtCore.SIGNAL('file_done'), self.update_recent_file_gps)
                self.connect(self.copyThread, QtCore.SIGNAL('completed'), self.reset_cursor)
            self.copyThread.start()

    @ex_deco
    def submitImage(self):
        # Get path and domain from parent
        path   = self.parent.path_list[0]
        domain = '%s/images/submit' % (self.parent.domain)

        # Get data from form
        car_number    = str(self.imageForm.numberInput.currentText())
        car_color     = str(self.imageForm.colorInput.currentText())
        person_letter = str(self.imageForm.letterInput.currentText())
        time_hour     = str(self.imageForm.timeInput.time().hour())
        time_minute   = str(self.imageForm.timeInput.time().minute())

        # Establish source and destination folders
        src_directory = ensure_structure(path, 'images', car_number, car_color, person_letter)
        dst_directory = ensure_structure(path, 'zip', car_number, car_color)

        # Gather selected images from the GUI
        first   = self.parent.imageDisplay.first_image.current_image
        last    = self.parent.imageDisplay.last_image.current_image
        zebra   = []
        giraffe = []
        for IB in self.parent.imageDisplay.image_boxes:
            (select_path, select_type) = IB.get_selection()
            if select_type == 'Unassigned':
                raise IOError('Please make sure all image boxes have been identified as either zebra of giraffe.')
                return
            elif select_type == 'Zebra':
                zebra.append(select_path)
            elif select_type == 'Giraffe':
                giraffe.append(select_path)
            elif select_type == 'Ignore':
                pass

        # Make empty if needed
        if len(zebra) == 0 or len(giraffe) == 0:
            with open(join(src_directory, '.empty'), 'w') as empty:
                empty.write('')

        # Create zip archive
        zip_path = join(dst_directory, person_letter + '.zip')
        with zipfile.ZipFile(zip_path, 'w') as zip_archive:
            zip_archive.write(join(src_directory, first), 'first.jpg')
            zip_archive.write(join(src_directory, last), 'last.jpg')
            if len(zebra) == 0:
                zip_archive.write(join(src_directory, '.empty'), join('zebra', '.empty'))
            if len(giraffe) == 0:
                zip_archive.write(join(src_directory, '.empty'), join('giraffe', '.empty'))
            for filename in zebra:
                zip_archive.write(join(src_directory, filename), join('zebra', filename))
            for filename in giraffe:
                zip_archive.write(join(src_directory, filename), join('giraffe', filename))

        # Format data
        data = {
            'car_color': car_color,
            'car_number': car_number,
            'person_letter': person_letter,
            'image_first_time_hour': time_hour,
            'image_first_time_minute': time_minute,
        }
        content = open(zip_path, 'rb')
        files = {
            'image_archive': content,
        }

        # Send POST request
        r = requests.post(domain, data=data, files=files)

        # Response
        response = json.loads(r.text)
        if response['status']['code'] != 0:
            self.complete_image_step_6 = False
            self.updateStatus()
            raise IOError('Server responded with an error' + response['status']['message'])
        self.complete_image_step_6 = True
        self.updateStatus()

    @ex_deco
    def submitGPS(self):
        # Get path and domain from parent
        path   = self.parent.path_list[0]
        domain = '%s/gps/submit' % (self.parent.domain)

        # Get data from form
        car_number    = str(self.gpsForm.numberInput.currentText())
        car_color     = str(self.gpsForm.colorInput.currentText())
        time_hour     = str(self.gpsForm.timeInput.time().hour())
        time_minute   = str(self.gpsForm.timeInput.time().minute())

        # Establish source folder
        src_directory = ensure_structure(path, 'gps', car_number, car_color)

        # Format data
        data = {
            'car_color': car_color,
            'car_number': car_number,
            'gps_start_time_hour': time_hour,
            'gps_start_time_minute': time_minute,
        }
        content = open(join(src_directory, 'track.gpx'), 'rb')
        files = {
            'gps_data': content,
        }

        # Send POST request
        r = requests.post(domain, data=data, files=files)

        # Response
        response = json.loads(r.text)
        if response['status']['code'] != 0:
            self.complete_gps_step_4 = False
            self.updateStatus()
            raise IOError('Server responded with an error' + response['status']['message'])
        self.complete_gps_step_4 = True
        self.updateStatus()

    def clear(self):
        # Reset cursor
        QtGui.QApplication.restoreOverrideCursor()
        self.sidebarStatus.setText('')
        # Stop any ongoing copy thread
        if self.copyThread is not None:
            self.copyThread.terminate()
            self.copyThread.quit()
        # Clear attributes
        self.import_directory = None
        self.image_file_list = []
        self.gps_file_list = []
        # Clear Flags
        self.complete_image_step_1 = False
        self.complete_image_step_2 = False
        self.complete_image_step_3_name = False
        self.complete_image_step_3_time = False
        self.complete_image_step_4 = False
        self.complete_image_step_5 = False
        self.complete_image_step_6 = None
        self.complete_gps_step_1 = False
        self.complete_gps_step_2 = False
        self.complete_gps_step_3 = False
        self.complete_gps_step_4 = None
        # Update overall display
        if self.parent.currentDisplay == 0:
            # Clear imageForm and imageDisplay
            self.imageForm.clear()
            self.parent.clearImageDisplay()
            self.imageForm.show()
            self.gpsForm.hide()
        elif self.parent.currentDisplay == 1:
            # Clear gpsForm and gpsDisplay
            self.gpsForm.clear()
            self.parent.clearGPSDisplay()
            self.imageForm.hide()
            self.gpsForm.show()
        # Update status
        self.updateStatus()

    def imagesSelectedOverride(self, imgList):
        # possibly do more tests for validity of list here
        self.clear()
        self.import_directory = "overridden"
        self.imageForm.driveLabel.setText("Images selected manually...")
        self.complete_image_step_1 = True
        self.image_file_list = imgList
        self.updateStatus()


class ImageForm(QtGui.QWidget, Ui_ImageForm):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self)
        self.parent = parent
        self.setupUi(self)
        self.initWidgets()
        self.initConnect()

    def initWidgets(self):
        self.numberInput.addItems(CAR_NUMBER)
        self.letterInput.addItems(PERSON_LETTERS)
        self.colorInput = QwwColorComboBox()
        self.colorInputContainer.addWidget(self.colorInput)
        for (color_name, color_hex) in CAR_COLORS:
            color = QtGui.QColor(color_hex)
            self.colorInput.addColor(color, color_name)
        self.driveBrowse.setIcon(QtGui.QIcon(BROWSE_ICON))

    def initConnect(self):
        self.driveBrowse.clicked.connect(self.open_directory)
        self.colorInput.currentIndexChanged[int].connect(self.check_identification)
        self.numberInput.currentIndexChanged[int].connect(self.check_identification)
        self.letterInput.currentIndexChanged[int].connect(self.check_identification)
        self.nameInput.textEdited.connect(self.check_sync_name)
        self.timeInput.timeChanged.connect(self.check_sync_time)

    # Slots
    def check_identification(self, ignore):
        color_index  = self.colorInput.currentIndex()
        number_index = self.numberInput.currentIndex()
        letter_index = self.letterInput.currentIndex()
        if color_index > 0 and number_index > 0 and letter_index > 0:
            self.parent.complete_image_step_2 = True
        else:
            self.parent.complete_image_step_2 = False
        self.parent.updateStatus()

    def check_sync_name(self, value):
        if len(value) > 0:
            self.parent.complete_image_step_3_name = True
        else:
            self.parent.complete_image_step_3_name = False
        self.parent.updateStatus()

    def check_sync_time(self, value):
        hour = int(str(value.hour()))
        if hour in TIME_HOUR_RANGE:
            self.parent.complete_image_step_3_time = True
        else:
            self.parent.complete_image_step_3_time = False
        self.parent.updateStatus()

    # Functions
    def open_directory(self):
        def truncate(path):
            if len(directory) > 40:
                return '...' + directory[-40:]
            else:
                return directory
        directory = str(QtGui.QFileDialog.getExistingDirectory(self, 'Select Directory'))
        if len(directory) > 0:
            self.driveLabel.setText(truncate(directory))
            self.parent.complete_image_step_1 = True
        else:
            self.parent.complete_image_step_1 = False
        self.parent.import_directory = directory
        self.parent.updateStatus()

    def clear(self):
        self.driveLabel.setText('Select a Directory...')
        self.colorInput.setCurrentIndex(0)
        self.numberInput.setCurrentIndex(0)
        self.letterInput.setCurrentIndex(0)
        self.nameInput.setText('')
        self.timeInput.setTime(QtCore.QTime(0, 0, 0, 0))


class GPSForm(QtGui.QWidget, Ui_GPSForm):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self)
        self.parent = parent
        self.setupUi(self)
        self.initWidgets()
        self.initConnect()

    def initWidgets(self):
        self.colorInput = QwwColorComboBox()
        self.colorInputContainer.addWidget(self.colorInput)
        self.numberInput.addItems(CAR_NUMBER)
        for (color_name, color_hex) in CAR_COLORS:
            color = QtGui.QColor(color_hex)
            self.colorInput.addColor(color, color_name)

    def initConnect(self):
        self.colorInput.currentIndexChanged[int].connect(self.check_identification)
        self.numberInput.currentIndexChanged[int].connect(self.check_identification)
        self.timeInput.timeChanged.connect(self.check_sync_time)

    # Slots
    def check_identification(self, ignore):
        color_index  = self.colorInput.currentIndex()
        number_index = self.numberInput.currentIndex()
        if color_index > 0 and number_index > 0:
            self.parent.complete_gps_step_1 = True
        else:
            self.parent.complete_gps_step_1 = False
        self.parent.updateStatus()

    def check_sync_time(self, value):
        hour = int(str(value.hour()))
        if hour in TIME_HOUR_RANGE:
            self.parent.complete_gps_step_2 = True
        else:
            self.parent.complete_gps_step_2 = False
        self.parent.updateStatus()

    # Functions
    def clear(self):
        self.colorInput.setCurrentIndex(0)
        self.numberInput.setCurrentIndex(0)
        self.timeInput.setTime(QtCore.QTime(0, 0, 0, 0))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    widget = Sidebar()
    widget.show()
    sys.exit(app.exec_())
