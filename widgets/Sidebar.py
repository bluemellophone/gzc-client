import sys
from PyQt4 import QtCore, QtGui
from SidebarSkel import Ui_Sidebar
from ImageFormSkel import Ui_ImageForm
from GPSFormSkel import Ui_GPSForm
from GZCQWidgets import QwwColorComboBox
from os.path import dirname, join, basename, exists
from shutil import rmtree
from clientfuncs import CopyThread, find_candidates, ex_deco


LOGO_SIZE = 150
FILE_DPATH = dirname(__file__)
LOGO_ZERO = join(FILE_DPATH, '../assets/logo_kwf_alpha.png')
LOGO_ONE = join(FILE_DPATH, '../assets/logo_ibeis_alpha.png')
LOGO_TWO = join(FILE_DPATH, '../assets/logo_kws_alpha.png')
IMPORT_ICON = join(FILE_DPATH, '../assets/icons/icon_import.png')
SUBMIT_ICON = join(FILE_DPATH, '../assets/icons/icon_upload.png')
BROWSE_ICON = join(FILE_DPATH, '../assets/icons/icon_browse.png')
CLEAR_ICON = join(FILE_DPATH, '../assets/icons/icon_trash.png')

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


class Sidebar(QtGui.QWidget, Ui_Sidebar):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self)
        self.parent = parent
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
        logo0 = QtGui.QPixmap(LOGO_ZERO)
        # logo1 = QtGui.QPixmap(LOGO_ONE).scaled(QtCore.QSize(LOGO_SIZE, LOGO_SIZE), QtCore.Qt.KeepAspectRatio)
        # logo2 = QtGui.QPixmap(LOGO_TWO).scaled(QtCore.QSize(LOGO_SIZE, LOGO_SIZE), QtCore.Qt.KeepAspectRatio)
        self.logo0.setPixmap(logo0)
        # self.logo1.setPixmap(logo1)
        # self.logo2.setPixmap(logo2)

    def initConnect(self):
        self.submitButton.clicked.connect(self.submitClicked)
        self.clearButton.clicked.connect(self.clearClicked)

    def initVisuals(self):
        # Setup clear icon
        self.clearButton.setText('')
        self.clearButton.setIcon(QtGui.QIcon(CLEAR_ICON))
        # Hide non-visible icons
        self.logo1.setMaximumHeight(0)
        self.logo2.setMaximumHeight(0)
        # Clear Sidebar
        self.clear()

    # Slots
    @ex_deco
    def submitClicked(self, *args):
        if self.parent.currentDisplay == 0:
            if self.complete_image_step_4:
                print('COMPILE ZIP')
            else:
                car_number = str(self.imageForm.numberInput.currentText())
                car_color = str(self.imageForm.colorInput.currentText())
                person_letter = str(self.imageForm.letterInput.currentText())
                QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
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
                self.files = find_candidates(directory, str(self.imageForm.nameInput.text()))
                if len(self.files) == 0:
                    self.reset_cursor()
                    raise IOError('Could not find any files for selected directory. Please check your first image name.')
                    return
                #send this file list to the selection group i am a bad programmer
                self.file_bases = [basename(f) for f in self.files]
                # print self.file_bases
                self.move_file_list(self.file_bases)

                target_directory = join('..', 'data', 'images', car_number + car_color, person_letter)
                if exists(target_directory):
                    print("Target directory already exists... deleting")
                    rmtree(target_directory)
                self.copyThread = CopyThread(self.files, [target_directory])
                self.connect(self.copyThread, QtCore.SIGNAL('file_done'), self.update_recent_file)
                self.connect(self.copyThread, QtCore.SIGNAL('completed'), self.reset_cursor)
                self.copyThread.start()
        elif self.parent.currentDisplay == 1:
            print('START IMPORT')

    def clearClicked(self):
        self.clear()

    # Functions
    def updateStatus(self):
        if self.parent.currentDisplay == 0:
            # Image - Step 0 (always show)
            self.imageForm.driveLayout.show()
            # Image - Step 1
            if self.complete_image_step_1:
                self.imageForm.idLayout.show()
            else:
                self.imageForm.idLayout.hide()
            # Image - Step 2
            if self.complete_image_step_2:
                self.imageForm.syncLayout.show()
            else:
                self.imageForm.syncLayout.hide()
            # Image - Step 3
            if self.complete_image_step_3:
                self.submitButton.setEnabled(True)
            else:
                self.submitButton.setEnabled(False)
            # Image - Step 4 (Images)
            if self.complete_image_step_4:
                self.submitButton.setIcon(QtGui.QIcon(SUBMIT_ICON))
                self.submitButton.setText("Submit")
            else:
                self.submitButton.setIcon(QtGui.QIcon(IMPORT_ICON))
                self.submitButton.setText("Import")

            # CHECK IMAGES
            # print("TODO:", self.parent.allImagesSelected())
        elif self.parent.currentDisplay == 1:
            # GPS - Step 0 (always show)
            self.gpsForm.idLayout.show()
            # GPS - Step 1
            if self.complete_gps_step_1:
                self.gpsForm.syncLayout.show()
                self.submitButton.setEnabled(True)
            else:
                self.gpsForm.syncLayout.hide()
                self.submitButton.setEnabled(False)

    def move_file_list(self, file_list):
        self.parent.imageDisplay.first_image.current_image = file_list.pop(0)
        self.parent.imageDisplay.last_image.current_image = file_list.pop()
        # self.image_selection_group.stored_files = file_list

    def update_recent_file(self, filename):
        #self.progress_bar.setText('Imported new image from ' + filename)
        self.parent.imageDisplay.add_filename(filename)

    def reset_cursor(self):
        QtGui.QApplication.restoreOverrideCursor()

    def clear(self):
        # Clear Flags
        self.import_directory = None
        self.complete_image_step_1 = False
        self.complete_image_step_2 = False
        self.complete_image_step_3 = False
        self.complete_image_step_4 = False
        self.complete_gps_step_1 = False
        self.complete_gps_step_2 = False
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
        self.nameInput.textEdited.connect(self.check_sync)

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

    def check_sync(self, value):
        if len(value) > 0:
            self.parent.complete_image_step_3 = True
        else:
            self.parent.complete_image_step_3 = False
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

    # Slots
    def check_identification(self, ignore):
        color_index  = self.colorInput.currentIndex()
        number_index = self.numberInput.currentIndex()
        if color_index > 0 and number_index > 0:
            self.parent.complete_gps_step_1 = True
        else:
            self.parent.complete_gps_step_1 = False
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
