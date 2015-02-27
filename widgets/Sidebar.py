from __future__ import absolute_import, division, print_function
import sys
from PyQt4 import QtCore, QtGui
from widgets.SidebarSkel import Ui_Sidebar
from widgets.ImageFormSkel import Ui_ImageForm
from widgets.GPSFormSkel import Ui_GPSForm
from widgets.GZCQWidgets import QwwColorComboBox
from os.path import join, basename, exists
from shutil import rmtree
import utool as ut
from clientfuncs import CopyFiles, ExtractGPS, find_candidates, ex_deco, ensure_structure, resource_path
import zipfile
import random
import simplejson as json
import requests


LOGO_SIZE      = 200
LOGO           = resource_path(join('assets', 'logo_ibeis_alpha.png'))
# LOGO           = resource_path(join('assets', 'logo_kwf_alpha.png'))
# LOGO           = resource_path(join('assets', 'logo_kws_alpha.png'))
IMPORT_ICON    = resource_path(join('assets', 'icons', 'icon_import.png'))
BROWSE_ICON    = resource_path(join('assets', 'icons', 'icon_browse.png'))
CLEAR_ICON     = resource_path(join('assets', 'icons', 'icon_trash.png'))
WAITING_ICON   = resource_path(join('assets', 'icons', 'icon_trash.png'))
SUBMIT_ICON    = resource_path(join('assets', 'icons', 'icon_upload.png'))
ACCEPTED_ICON  = resource_path(join('assets', 'icons', 'icon_accepted.png'))
REJECTED_ICON  = resource_path(join('assets', 'icons', 'icon_rejected.png'))
RESOURCE_PATH  = ut.get_app_resource_dir('gzc-client')
RESOURCE_EMPTY = join(RESOURCE_PATH, '.empty')
DIRECTORY_OVERRIDE_STR   = '<<<override>>>'
RESOURCE_TEMPORARY_TRACK = join(RESOURCE_PATH, 'track.gpx')

CAR_COLORS_COMBO    = [('Select Color', '#F6F6F6')] + [
    ('white',    '#FFFFFF'),
    ('red',        '#D9534F'),
    ('orange', '#EF7A4C'),
    ('yellow', '#F0AD4E'),
    ('green',    '#5CB85C'),
    ('blue',     '#3071A9'),
    ('purple', '#6F5499'),
    ('black',    '#333333'),
]
CAR_COLORS              = [ color[0] for color in CAR_COLORS_COMBO[1:] ]
CAR_NUMBERS             = map(str, range(1, 26))  # 51
CAR_NUMBERS_COMBO       = ['Select Number'] + CAR_NUMBERS
PERSON_LETTERS          = ['a', 'b', 'c', 'd', 'e', 'f']  # , 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'aa', 'bb', 'cc', 'dd', 'ee', 'ff', 'gg', 'hh', 'ii', 'jj', 'kk', 'll', 'mm', 'nn', 'oo', 'pp', 'qq', 'rr', 'ss', 'tt', 'uu', 'vv', 'ww', 'xx', 'yy', 'zz']
PERSON_LETTERS_COMBO    = ['Select Letter'] + PERSON_LETTERS
TIME_HOUR_RANGE         = map(str, range(6, 23))
TIME_HOUR_RANGE_COMBO   = ['Hour'] + TIME_HOUR_RANGE
TIME_MINUTE_RANGE       = map(str, range(0, 60))
TIME_MINUTE_RANGE_COMBO = ['Minute'] + TIME_MINUTE_RANGE
TRACK_RANGE             = map(str, range(1, 6))
TRACK_RANGE_COMBO       = ['Select Track'] + TRACK_RANGE


PALETTE_BASE = '''
    font: 35px;
    margin: 0 1px 0 1px;
    border-style: groove;
    border-width: 1px;
'''
PALETTE_CLEAR = '''
    margin-left: 10px;
    color: #333333;
    border-color: #da534f;
'''
PALETTE_DEFAULT = '''
    color: #333333;
    border-color: #afafaf;
'''
PALETTE_SUBMIT =  '''
    color: #ffffff;
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #2198c0, stop: 1 #0c457e);
    border-color: #0c457e;
'''
PALETTE_ACCEPT =  '''
    color: #ffffff;
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #5cb85c, stop: 1 #4cae4c);
    border-color: #4cae4c;
'''
PALETTE_REJECT =  '''
    color: #ffffff;
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #d9534f, stop: 1 #d43f3a);
    border-color: #d43f3a;
'''


class Sidebar(QtGui.QWidget, Ui_Sidebar):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self)
        self.parent     = parent
        self.CopyFiles  = None
        self.ExtractGPS = None
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
        # Set clear button palette
        self.clearButton.setStyleSheet(PALETTE_BASE + PALETTE_CLEAR)
        # Clear Sidebar
        self.clear()

    # Slots
    def submitClicked(self, *args):
        if self.currentDisplay() == 0:
            if self.imageStatus < 8:
                self.copyImages()
            else:
                self.submitImages()
        elif self.currentDisplay() == 1:
            if self.gpsStatus < 5:
                self.copyGPS()
            else:
                self.submitGPS()

    def clearClicked(self):
        self.clear()

    # Convenience
    @ex_deco
    def setSubmitButtonLook(self, text=None, icon=None, palette=None):
        if text is not None:
            self.submitButton.setText(text)
        if icon is not None:
            self.submitButton.setIcon(QtGui.QIcon(icon))
        if palette is not None:
            self.submitButton.setStyleSheet(PALETTE_BASE + palette)

    @ex_deco
    def currentDisplay(self):
        return self.parent.currentDisplay

    @ex_deco
    def clearCursor(self):
        QtGui.QApplication.restoreOverrideCursor()
        self.updateStatus()

    @ex_deco
    def setWaitCursor(self):
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

    @ex_deco
    def copyFilesImageCopied(self, index, length, filename):
        self.sidebarStatus.setText('Copying Image %s / %s' % (index, length, ))
        add_to_display = index in self.imageImportFilesRandomIndices
        self.parent.imageDisplay.add_filename(filename, add_to_display=add_to_display)

    @ex_deco
    def copyFilesGPSCopied(self, index, length, filename):
        # print('CAUGHT %s %s' % (index, length, ))
        self.sidebarStatus.setText('Copying Track %s / %s' % (index, length, ))

    @ex_deco
    def copyFilesCompleted(self, filenames):
        if self.currentDisplay() == 0:
            self.imageCopied = True
        elif self.currentDisplay() == 1:
            self.gpsCopied = True
        self.clearCursor()

    @ex_deco
    def copyFilesException(self, exception):
        # This is to throw the exception and ex_deco in the correct thread
        self.clearCursor()
        raise exception

    @ex_deco
    def extractGPSException(self, exception):
        # This is to throw the exception and ex_deco in the correct thread
        self.clearCursor()
        raise exception

    @ex_deco
    def extractGPSCompleted(self, gpx_content):
        with open(RESOURCE_TEMPORARY_TRACK, 'w') as track:
            track.write(gpx_content)
        self.copyGPX(RESOURCE_TEMPORARY_TRACK)

    # Functions
    def updateStatus(self):
        self.sidebarStatus.setText('')
        self.submitButton.setEnabled(False)
        self.setSubmitButtonLook('Fill Form', IMPORT_ICON, PALETTE_DEFAULT)
        self.imageStatus = 0
        self.gpsStatus = 0
        if self.currentDisplay() == 0:
            # Show base case elements
            self.imageForm.driveLayout.show()
            self.imageForm.idLayout.hide()
            self.imageForm.syncLayout.hide()
            self.imageForm.nameInput.setEnabled(True)
            # Gather form values
            carNumber    = self.imageForm.getNumber()
            carColor     = self.imageForm.getColor()
            personLetter = self.imageForm.getLetter()
            imageName    = self.imageForm.getImageName()
            timeHour     = self.imageForm.getHour()
            # Image - Step 1
            if self.imageImportDirectory is None:
                self.sidebarStatus.setText('Specify the SD Card directory')
                return
            self.imageStatus += 1
            self.imageForm.idLayout.show()
            # Image - Step 2
            if carNumber not in CAR_NUMBERS:
                self.sidebarStatus.setText('Specify the car number')
                return
            self.imageStatus += 1
            if carColor not in CAR_COLORS:
                self.sidebarStatus.setText('Specify the car color')
                return
            self.imageStatus += 1
            if personLetter not in PERSON_LETTERS:
                self.sidebarStatus.setText('Specify the person letter')
                return
            self.imageStatus += 1
            self.imageForm.syncLayout.show()
            if self.imageImportDirectory == DIRECTORY_OVERRIDE_STR:
                self.imageForm.nameInput.setEnabled(False)
            # Image - Step 3 (Copy Images)
            if imageName == '':
                self.sidebarStatus.setText('Specify the image name to search')
                return
            self.imageStatus += 1
            self.submitButton.setEnabled(True)
            self.setSubmitButtonLook('Import Images', IMPORT_ICON)
            # Image - Step 4 (Sync and Select)
            if not self.imageCopied:
                self.sidebarStatus.setText('Import the card\'s images')
                return
            self.imageStatus += 1
            self.submitButton.setEnabled(False)
            self.setSubmitButtonLook('Images Imported', WAITING_ICON, PALETTE_DEFAULT)
            if timeHour not in TIME_HOUR_RANGE:
                self.sidebarStatus.setText('Specify the sync time hour and minute')
                return
            self.imageStatus += 1
            if not self.parent.allImagesSelected():
                self.sidebarStatus.setText('Select the species for all images')
                return
            self.imageStatus += 1
            self.submitButton.setEnabled(True)
            self.setSubmitButtonLook('Submit Images', SUBMIT_ICON, PALETTE_SUBMIT)
            # Image - Step 5 (Submit)
            if self.imageSubmitted is None:
                self.sidebarStatus.setText('Submit the images for processing')
                return
            self.imageStatus += 1
            if self.imageSubmitted:
                self.setSubmitButtonLook('Images Accepted', ACCEPTED_ICON, PALETTE_ACCEPT)
            else:
                self.setSubmitButtonLook('Images Rejected', REJECTED_ICON, PALETTE_REJECT)
            self.imageStatus += 1
            self.submitButton.setEnabled(False)
            self.sidebarStatus.setText('Clear the form to start the next submission')
        elif self.currentDisplay() == 1:
            # Show base case elements
            self.gpsForm.idLayout.show()
            self.gpsForm.syncLayout.hide()
            # Gather form values
            carNumber    = self.gpsForm.getNumber()
            carColor     = self.gpsForm.getColor()
            timeHour     = self.gpsForm.getHour()
            trackNumber  = self.gpsForm.getTrack()
            # GPS - Step 1
            if carNumber not in CAR_NUMBERS:
                self.sidebarStatus.setText('Specify the car number')
                return
            self.gpsStatus += 1
            if carColor not in CAR_COLORS:
                self.sidebarStatus.setText('Specify the car color')
                return
            self.gpsStatus += 1
            self.gpsForm.syncLayout.show()
            # GPS - Step 3 (Copy GPSs)
            self.submitButton.setEnabled(True)
            self.setSubmitButtonLook('Import Track', IMPORT_ICON)
            # GPS - Step 4 (Sync and Select)
            if not self.gpsCopied:
                self.sidebarStatus.setText('Import the dongle\'s GPS track')
                return
            self.gpsStatus += 1
            self.submitButton.setEnabled(False)
            self.setSubmitButtonLook('Track Imported', WAITING_ICON, PALETTE_DEFAULT)
            if timeHour not in TIME_HOUR_RANGE:
                self.sidebarStatus.setText('Specify the sync time hour and minute')
                return
            self.gpsStatus += 1
            if trackNumber not in TRACK_RANGE:
                self.sidebarStatus.setText('Specify the track number')
                return
            self.gpsStatus += 1
            self.submitButton.setEnabled(True)
            self.setSubmitButtonLook('Submit Track', SUBMIT_ICON, PALETTE_SUBMIT)
            # Image - Step 5 (Submit)
            if self.gpsSubmitted is None:
                self.sidebarStatus.setText('Submit the GPS track for processing')
                return
            self.gpsStatus += 1
            if self.gpsSubmitted:
                self.setSubmitButtonLook('Track Accepted', ACCEPTED_ICON, PALETTE_ACCEPT)
            else:
                self.setSubmitButtonLook('Track Rejected', REJECTED_ICON, PALETTE_REJECT)
            self.gpsStatus += 1
            self.submitButton.setEnabled(False)
            self.sidebarStatus.setText('Clear the form to start the next submission')

    def clear(self, clearCopyCache=True, ignoreImage=False, ignoreGPS=False):
        # Always clear these attributes
        self.imageCopied = False
        self.gpsCopied = False
        self.imageSubmitted = None  # None because we use booleans for error checking
        self.gpsSubmitted = None  # None because we use booleans for error checking
        self.imageImportFilesRandomIndices = set()
        if clearCopyCache:
            # Clear copy cache
            self.imageImportDirectory = None
            self.imageImportFiles = []
            self.gpsImportFiles = []
        # Stop any ongoing copy or extract thread
        if self.CopyFiles is not None:
            self.CopyFiles.terminate()
            self.CopyFiles.quit()
        if self.ExtractGPS is not None:
            self.ExtractGPS.terminate()
            self.ExtractGPS.quit()
        # Update overall display
        if self.currentDisplay() == 0:
            if not ignoreImage:
                self.imageForm.clear()
            self.parent.clearImageDisplay()
            self.imageForm.show()
            self.gpsForm.hide()
        elif self.currentDisplay() == 1:
            if not ignoreGPS:
                self.gpsForm.clear()
            self.parent.clearGPSDisplay()
            self.imageForm.hide()
            self.gpsForm.show()
        # Clear cursor, which calls updateStatus
        self.clearCursor()

    # Images
    @ex_deco
    def imageManualSelection(self, filepaths):
        if len(filepaths) < 3:
            raise IOError('Please select at least three images to import when manually selecting images (fisrt, last and at least one query image)')
        self.clear()
        self.imageImportDirectory = DIRECTORY_OVERRIDE_STR
        self.imageImportFiles = filepaths
        self.imageForm.driveLabel.setText('Manual Selection')
        self.imageForm.nameInput.setText(basename(self.imageImportFiles[0]))
        self.updateStatus()

    @ex_deco
    def copyImages(self):
        self.clear(clearCopyCache=False, ignoreImage=True)
        self.setWaitCursor()
        # Get information from form
        carNumber    = self.imageForm.getNumber()
        carColor     = self.imageForm.getColor()
        personLetter = self.imageForm.getLetter()
        imageName    = self.imageForm.getImageName()
        # Sanity checks (round 1)
        if self.imageImportDirectory is None or self.imageImportDirectory == '':
            self.clearCursor()
            raise IOError('Please select the directory that contains the photos you wish to import from')
        if carNumber not in CAR_NUMBERS or carColor not in CAR_COLORS or personLetter not in PERSON_LETTERS:
            self.clearCursor()
            raise IOError('Please select the correct car number, color and person letter')
        if imageName == '':
            self.clearCursor()
            raise IOError('The first image name must be defined')
        # Find candidates if searching
        if self.imageImportDirectory != DIRECTORY_OVERRIDE_STR:
            self.imageImportFiles = find_candidates(self.imageImportDirectory, imageName)
        # Sanity checks (round 2)
        if len(self.imageImportFiles) == 0:
            self.clearCursor()
            raise IOError('Could not find any files for selected directory. Please check your first image name')
        # Create random indices
        while len(self.imageImportFilesRandomIndices) < min(10, len(self.imageImportFiles)):
            index = random.randint(0, len(self.imageImportFiles) - 1)
            self.imageImportFilesRandomIndices.add(index)
        # Set the first and last images
        filenames = [basename(f) for f in self.imageImportFiles]
        self.parent.setImageDisplayFirstImage(filenames.pop(0))
        self.parent.setImageDisplayLastImage(filenames.pop())
        # Ensure path exists for all destinations
        destinationPaths = []
        for index, path in enumerate(self.parent.backupDestinationPaths):
            personPath = ensure_structure(path, 'images', carNumber, carColor, personLetter)
            if exists(personPath):
                print('Target person directory already exists... deleting')
                rmtree(personPath)
            destinationPaths.append(personPath)
        # Start copy thread
        self.CopyFiles = CopyFiles(self.imageImportFiles, destinationPaths)
        self.connect(self.CopyFiles, QtCore.SIGNAL('fileCopied'), self.copyFilesImageCopied)
        self.connect(self.CopyFiles, QtCore.SIGNAL('completed'), self.copyFilesCompleted)
        self.connect(self.CopyFiles, QtCore.SIGNAL('__EXCEPTION__'), self.copyFilesException)
        self.CopyFiles.start()

    @ex_deco
    def submitImages(self):
        # Get path and domain from parent
        path   = self.parent.backupDestinationPaths[0]
        domain = '%s/images/submit' % (self.parent.domain)
        # Get data from form
        carNumber    = self.imageForm.getNumber()
        carColor     = self.imageForm.getColor()
        personLetter = self.imageForm.getLetter()
        timeHour     = self.imageForm.getHour()
        timeMinute   = self.imageForm.getMinute()
        # Establish source and destination folders
        srcDirectory = ensure_structure(path, 'images', carNumber, carColor, personLetter)
        dstDirectory = ensure_structure(path, 'zip', carNumber, carColor)
        # Gather selected images from the GUI
        first   = self.parent.getImageDisplayFirstImage()
        last    = self.parent.getImageDisplayLastImage()
        zebra   = []
        giraffe = []
        for IB in self.parent.getImageDisplayImageBoxes():
            (select_path, select_type) = IB.get_selection()
            if select_type == 'Unassigned':
                raise IOError('Please make sure all image boxes have been identified as either zebra of giraffe')
                return
            elif select_type == 'Zebra':
                zebra.append(select_path)
            elif select_type == 'Giraffe':
                giraffe.append(select_path)
            elif select_type == 'Ignore':
                pass
        # Make empty file
        if not exists(RESOURCE_EMPTY):
            with open(RESOURCE_EMPTY, 'w') as empty:
                empty.write('')
        # Create zip archive
        zip_path = join(dstDirectory, personLetter + '.zip')
        with zipfile.ZipFile(zip_path, 'w') as zip_archive:
            zip_archive.write(join(srcDirectory, first), 'first.jpg')
            zip_archive.write(join(srcDirectory, last), 'last.jpg')
            if len(zebra) == 0:
                zip_archive.write(RESOURCE_EMPTY, join('zebra', '.empty'))
            if len(giraffe) == 0:
                zip_archive.write(RESOURCE_EMPTY, join('giraffe', '.empty'))
            for filename in zebra:
                zip_archive.write(join(srcDirectory, filename), join('zebra', filename))
            for filename in giraffe:
                zip_archive.write(join(srcDirectory, filename), join('giraffe', filename))
        # Format data
        data = {
            'car_number': carNumber,
            'car_color': carColor,
            'person_letter': personLetter,
            'image_first_time_hour': timeHour,
            'image_first_time_minute': timeMinute,
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
            self.imageSubmitted = False
            self.updateStatus()
            raise IOError('Server responded with an error: %r' % (response, ))
        self.imageSubmitted = True
        self.updateStatus()

    # GPS
    @ex_deco
    def copyGPX(self, preextractedGPXPath):
        # Get data from form
        carNumber = self.gpsForm.getNumber()
        carColor  = self.gpsForm.getColor()
        # Sanity checks
        if carNumber not in CAR_NUMBERS or carColor not in CAR_COLORS:
            self.clearCursor()
            raise IOError('Please select the correct car number and color')
        # Load GPX path
        self.gpsImportFiles = [preextractedGPXPath]
        with open(preextractedGPXPath) as gpxFile:
            gpxTrack = gpxFile.read()
            self.parent.displayGPXTrack(gpxTrack)
        # Ensure path exists for all destinations
        destinationPaths = []
        for index, path in enumerate(self.parent.backupDestinationPaths):
            carPath = ensure_structure(path, 'gps', carNumber, carColor)
            if exists(carPath):
                print('Target car directory already exists... deleting')
                rmtree(carPath)
            destinationPaths.append(carPath)
        # Start copy thread
        self.CopyFiles = CopyFiles(self.gpsImportFiles, destinationPaths)
        self.connect(self.CopyFiles, QtCore.SIGNAL('fileCopied'), self.copyFilesGPSCopied)
        self.connect(self.CopyFiles, QtCore.SIGNAL('completed'), self.copyFilesCompleted)
        self.connect(self.CopyFiles, QtCore.SIGNAL('__EXCEPTION__'), self.copyFilesException)
        self.CopyFiles.start()

    @ex_deco
    def copyGPS(self, preextractedGPXPath=None):
        self.clear(clearCopyCache=False, ignoreGPS=True)
        self.setWaitCursor()
        # Get data from form
        carNumber = self.gpsForm.getNumber()
        carColor  = self.gpsForm.getColor()
        # Sanity checks
        if carNumber not in CAR_NUMBERS or carColor not in CAR_COLORS:
            self.clearCursor()
            raise IOError('Please select the correct car number and color')
        # Extract the data from the GPS dongle or process the preextractedGPXPath
        if preextractedGPXPath is None:
            self.ExtractGPS = ExtractGPS()
            self.connect(self.ExtractGPS, QtCore.SIGNAL('trackExtracted'), self.copyFilesGPSCopied)
            self.connect(self.ExtractGPS, QtCore.SIGNAL('completed'), self.extractGPSCompleted)
            self.connect(self.ExtractGPS, QtCore.SIGNAL('__EXCEPTION__'), self.extractGPSException)
            self.ExtractGPS.start()
        else:
            self.copyGPX(preextractedGPXPath)

    @ex_deco
    def submitGPS(self):
        # Get path and domain from parent
        path   = self.parent.backupDestinationPaths[0]
        domain = '%s/gps/submit' % (self.parent.domain)
        # Get data from form
        carNumber    = self.gpsForm.getNumber()
        carColor     = self.gpsForm.getColor()
        timeHour     = self.gpsForm.getHour()
        timeMinute   = self.gpsForm.getMinute()
        trackNumber  = self.gpsForm.getTrack()
        # Establish source folder
        srcDirectory = ensure_structure(path, 'gps', carNumber, carColor)
        # Format data
        data = {
            'car_number': carNumber,
            'car_color': carColor,
            'gps_start_time_hour': timeHour,
            'gps_start_time_minute': timeMinute,
            'track_number': trackNumber,
        }
        content = open(join(srcDirectory, 'track.gpx'), 'rb')
        files = {
            'gps_data': content,
        }
        # Send POST request
        r = requests.post(domain, data=data, files=files)
        # Response
        response = json.loads(r.text)
        if response['status']['code'] != 0:
            self.gpsSubmitted = False
            self.updateStatus()
            raise IOError('Server responded with an error: %r' % (response, ))
        self.gpsSubmitted = True
        self.updateStatus()


class ImageForm(QtGui.QWidget, Ui_ImageForm):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self)
        self.parent = parent
        self.setupUi(self)
        self.initWidgets()
        self.initConnect()

    def initWidgets(self):
        self.numberInput.addItems(CAR_NUMBERS_COMBO)
        self.letterInput.addItems(PERSON_LETTERS_COMBO)
        self.colorInput = QwwColorComboBox()
        self.colorInputContainer.addWidget(self.colorInput)
        for (color_name, color_hex) in CAR_COLORS_COMBO:
            color = QtGui.QColor(color_hex)
            self.colorInput.addColor(color, color_name)
        self.driveBrowse.setIcon(QtGui.QIcon(BROWSE_ICON))
        self.timeHour.addItems(TIME_HOUR_RANGE_COMBO)
        self.timeMinute.addItems(TIME_MINUTE_RANGE_COMBO)

    def initConnect(self):
        self.driveBrowse.clicked.connect(self.browseDirectory)
        self.colorInput.currentIndexChanged[int].connect(self.parent.updateStatus)
        self.numberInput.currentIndexChanged[int].connect(self.parent.updateStatus)
        self.letterInput.currentIndexChanged[int].connect(self.parent.updateStatus)
        self.nameInput.textEdited.connect(self.parent.updateStatus)
        self.timeHour.currentIndexChanged[int].connect(self.parent.updateStatus)
        self.timeMinute.currentIndexChanged[int].connect(self.parent.updateStatus)

    # Slots
    def browseDirectory(self):
        def _truncate(path):
            if len(directory) > 40:
                return '...' + directory[-40:]
            else:
                return directory
        directory = str(QtGui.QFileDialog.getExistingDirectory(self, 'Select Directory'))
        if len(directory) > 0:
            self.driveLabel.setText(_truncate(directory))
            self.parent.imageImportDirectory = directory
            self.parent.updateStatus()

    # Convenience
    def getNumber(self):
        return str(self.numberInput.currentText())

    def getColor(self):
        return str(self.colorInput.currentText())

    def getLetter(self):
        return str(self.letterInput.currentText())

    def getHour(self):
        return str(self.timeHour.currentText())

    def getMinute(self):
        return str(self.timeMinute.currentText())

    def getImageName(self):
        return str(self.nameInput.text())

    # Functions
    @ex_deco
    def clear(self):
        self.driveLabel.setText('Select a Directory...')
        self.colorInput.setCurrentIndex(0)
        self.numberInput.setCurrentIndex(0)
        self.letterInput.setCurrentIndex(0)
        self.nameInput.setEnabled(True)
        self.nameInput.setText('')


class GPSForm(QtGui.QWidget, Ui_GPSForm):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self)
        self.parent = parent
        self.setupUi(self)
        self.initWidgets()
        self.initConnect()

    def initWidgets(self):
        self.timeHour.addItems(TIME_HOUR_RANGE_COMBO)
        self.timeMinute.addItems(TIME_MINUTE_RANGE_COMBO)
        self.colorInput = QwwColorComboBox()
        self.colorInputContainer.addWidget(self.colorInput)
        self.numberInput.addItems(CAR_NUMBERS_COMBO)
        for (color_name, color_hex) in CAR_COLORS_COMBO:
            color = QtGui.QColor(color_hex)
            self.colorInput.addColor(color, color_name)
        self.trackNumber.addItems(TRACK_RANGE_COMBO)

    def initConnect(self):
        self.colorInput.currentIndexChanged[int].connect(self.parent.updateStatus)
        self.numberInput.currentIndexChanged[int].connect(self.parent.updateStatus)
        self.timeHour.currentIndexChanged[int].connect(self.parent.updateStatus)
        self.timeMinute.currentIndexChanged[int].connect(self.parent.updateStatus)

    # Convenience
    def getNumber(self):
        return str(self.numberInput.currentText())

    def getColor(self):
        return str(self.colorInput.currentText())

    def getHour(self):
        return str(self.timeHour.currentText())

    def getMinute(self):
        return str(self.timeMinute.currentText())

    def getTrack(self):
        return str(self.trackNumber.currentText())

    # Functions
    @ex_deco
    def clear(self):
        self.colorInput.setCurrentIndex(0)
        self.numberInput.setCurrentIndex(0)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    widget = Sidebar()
    widget.show()
    sys.exit(app.exec_())
