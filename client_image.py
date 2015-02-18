from __future__ import absolute_import, division, print_function
from PyQt4 import QtCore, QtGui
from clientfuncs import CopyThread, QwwColorComboBox
from os import listdir, getcwd, path, chdir
import simplejson as json
import time
import random
import sys
import copy
import zipfile
import requests

#TODO:
# add status bar to bottom -- WIP

# class first_last_image(QtGui.QWidget):


CAR_COLORS = [
    ('white',  '#FFFFFF'),
    ('red',    '#D9534F'),
    ('orange', '#EF7A4C'),
    ('yellow', '#F0AD4E'),
    ('green',  '#5CB85C'),
    ('blue',   '#3071A9'),
    ('purple', '#6F5499'),
    ('black',  '#333333'),
]
CAR_NUMBER = map(str, range(1, 50))
PERSON_LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'aa', 'bb', 'cc', 'dd', 'ee', 'ff', 'gg', 'hh', 'ii', 'jj', 'kk', 'll', 'mm', 'nn', 'oo', 'pp', 'qq', 'rr', 'ss', 'tt', 'uu', 'vv', 'ww', 'xx', 'yy', 'zz']
TIME_HOUR = map(str, range(0, 24))
TIME_MINUTE = map(str, range(0, 60))


class first_last_image(QtGui.QFrame):
    DEFAULT_IMAGE = 'assets/reroll.png'
    def __init__(self, *args):
        apply(QtGui.QWidget.__init__, (self, ) + args)
        QtGui.QWidget.__init__(self)
        self.init_widgets()
        self.init_layout()

    def init_widgets(self):
        self.image = QtGui.QLabel()
        self.image.setScaledContents(True)
        Pixmap = QtGui.QPixmap((self.DEFAULT_IMAGE)).scaled(QtCore.QSize(150, 150))
        self.desiredsize = Pixmap.size()
        self.image.setAlignment(QtCore.Qt.AlignCenter)
        self.image.setPixmap(Pixmap)
        self.current_image = self.DEFAULT_IMAGE

        #border stuffff?
        self.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        self.setLineWidth(2)

        self.image_time = QtGui.QLabel("Awaiting images...", self)
        self.image_time.setAlignment(QtCore.Qt.AlignCenter)

        self.info_text = QtGui.QLabel("", self)
        self.info_text.setAlignment(QtCore.Qt.AlignCenter)

    def init_layout(self):
        grid = QtGui.QGridLayout()
        grid.addWidget(self.image, 0, 0, 1, 0)
        grid.addWidget(self.image_time, 2, 0, 1, 2)
        grid.addWidget(self.info_text, 3, 0, 1, 2)

        self.setLayout(grid)

    def update(self, filename):
        self.image.setPixmap(QtGui.QPixmap(filename).scaled(self.desiredsize))
        self.current_image = filename
        self.image_time.setText(time.strftime('%d/%m/%y, %H:%M:%S', time.gmtime(path.getmtime(self.current_image))))


class image_selection_roll(QtGui.QLabel):
    #Modify the QtGui.QLabel functionality to allow it to act like a button
    DEFAULT_IMAGE = 'assets/reroll.png'

    def __init__(self, *args):
        apply(QtGui.QLabel.__init__, (self, ) + args)
        QtGui.QLabel.__init__(self)
        #self.setScaledContents(True) #<--this causes the image displayed to be centered, but stretched. Aspect ratio not maintained
        Pixmap = QtGui.QPixmap((self.DEFAULT_IMAGE)).scaled(QtCore.QSize(150, 150))
        self.desiredsize = Pixmap.size()
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setPixmap(Pixmap)

        self.current_image = self.DEFAULT_IMAGE

    def mouseReleaseEvent(self, ev):
        self.emit(QtCore.SIGNAL('clicked()'))

    def changeImage(self, image_file):
        self.setPixmap(QtGui.QPixmap(image_file).scaled(self.desiredsize))
        self.current_image = image_file

    def get_timestamp(self):
        #lol need to ensure path consistancy!
        chdir(path.dirname(path.realpath(__file__)))

        if self.current_image == self.DEFAULT_IMAGE:
            return "Awaiting images..."
        else:
            return time.strftime('%d/%m/%y, %H:%M:%S', time.gmtime(path.getmtime(self.current_image)))


class image_selection_box(QtGui.QWidget):
    #One selection box. Contains the image and two buttons
    def __init__(self, *args):
        apply(QtGui.QWidget.__init__, (self, ) + args)
        QtGui.QWidget.__init__(self)

        self.init_widgets()
        self.init_layout()
        self.init_connect()

    def init_widgets(self):
        self.image = image_selection_roll(self)
        self.select_zebra = QtGui.QPushButton('Zebra', self)
        self.select_giraffe = QtGui.QPushButton('Giraffe', self)
        self.select_zebra.setCheckable(True)
        self.select_giraffe.setCheckable(True)

        self.select_group = QtGui.QButtonGroup(self)
        self.select_group.addButton(self.select_zebra)
        self.select_group.addButton(self.select_giraffe)

        self.image_time = QtGui.QLabel(self.image.get_timestamp(), self)
        self.image_time.setAlignment(QtCore.Qt.AlignCenter)

    def init_layout(self):
        grid = QtGui.QGridLayout()
        grid.addWidget(self.image, 0, 0, 1, 0)
        grid.addWidget(self.image_time, 2, 0, 1, 2)
        grid.addWidget(self.select_zebra, 3, 0)
        grid.addWidget(self.select_giraffe, 3, 1)

        self.setLayout(grid)

    def init_connect(self):
        self.connect(self.image, QtCore.SIGNAL('clicked()'), self.reroll)

    def reroll(self):
        #get new filename
        filename = self.parent().get_filename()

        self.image.changeImage(filename)

        self.image_time.setText(self.image.get_timestamp())
        #uncheck the buttons if image is rerolled
        checked = self.select_group.checkedButton()
        # print checked
        if checked is not None:
            #HACK to reset all checked states
            self.select_group.setExclusive(False)
            checked.setChecked(False)
            self.select_group.setExclusive(True)

    def get_selection(self):
        return (path.basename(self.image.current_image), self.select_group.checkedButton().text())


class selection_group(QtGui.QWidget):
    #The right side of the interface
    def __init__(self, *args):
        apply(QtGui.QWidget.__init__, (self, ) + args)
        QtGui.QWidget.__init__(self)
        self.init_widgets()
        self.init_layout()
        self.stored_files = []
        self.active_files = []
        # self.init_connect()

    def init_widgets(self):
        self.first_image = first_last_image(self)
        self.first_image.info_text.setText("First Image in Directory")
        self.image_boxes = []
        for i in range(10):
            self.image_boxes.append(image_selection_box(self))

        self.last_image = first_last_image(self)
        self.last_image.info_text.setText("Last Image in Directory")

    def init_layout(self):

        gridV = QtGui.QVBoxLayout()
        hor1 = QtGui.QHBoxLayout()
        hor2 = QtGui.QHBoxLayout()
        hor3 = QtGui.QHBoxLayout()
        hor1.addStretch(1)
        hor1.addWidget(self.first_image)
        hor1.addStretch(1)
        hor1.addWidget(self.image_boxes[0])
        hor1.addStretch(1)
        hor1.addWidget(self.image_boxes[1])
        hor1.addStretch(1)
        hor1.addWidget(self.image_boxes[2])
        hor1.addStretch(1)
        hor2.addStretch(1)
        hor2.addWidget(self.image_boxes[3])
        hor2.addStretch(1)
        hor2.addWidget(self.image_boxes[4])
        hor2.addStretch(1)
        hor2.addWidget(self.image_boxes[5])
        hor2.addStretch(1)
        hor2.addWidget(self.image_boxes[6])
        hor2.addStretch(1)
        hor3.addStretch(1)
        hor3.addWidget(self.image_boxes[7])
        hor3.addStretch(1)
        hor3.addWidget(self.image_boxes[8])
        hor3.addStretch(1)
        hor3.addWidget(self.image_boxes[9])
        hor3.addStretch(1)
        hor3.addWidget(self.last_image)
        hor3.addStretch(1)
        gridV.addStretch(1)
        gridV.addLayout(hor1)
        gridV.addStretch(1)
        gridV.addLayout(hor2)
        gridV.addStretch(1)
        gridV.addLayout(hor3)
        gridV.addStretch(1)

        self.setLayout(gridV)

    def add_filename(self, filename):
        self.active_files.append(filename)
        self.stored_files.append(filename)
        #for the first couple of images to be copied, we will update the displayed photos
        if len(self.stored_files) == 1:
            #FIRST IMAGE, add to the first image box
            self.first_image.update(filename)

        else:
            for IB in self.image_boxes:
                if IB.image.current_image == IB.image.DEFAULT_IMAGE:
                    IB.reroll()
                    break
        #if we've filled the image boxes, update the last image
        self.last_image.update(filename)

    def get_filename(self):
        if len(self.active_files) ==  0:
            # If we've run through all the filename, just blindly restart the q
            self.active_files = copy.deepcopy(self.stored_files)

        filename = self.active_files.pop((random.randrange(len(self.active_files))))
        return filename


class user_input(QtGui.QWidget):
    def __init__(self, *args):
        apply(QtGui.QWidget.__init__, (self, ) + args)
        QtGui.QWidget.__init__(self)
        self.init_widgets()
        self.init_layout()
        self.init_connect()

    def init_widgets(self):
        self.logo = QtGui.QLabel(self)
        self.logo.setPixmap(QtGui.QPixmap('assets/logo.png').scaled(QtCore.QSize(100, 100)))

        self.browse_label = QtGui.QLabel('1) Select Drive With SD card:', self)
        self.browse_button = QtGui.QPushButton('Browse', self)
        self.browse_text = QtGui.QLineEdit(self)

        self.id_label = QtGui.QLabel('2) Input Identification Information', self)
        self.id_car_label = QtGui.QLabel('Car Number:', self)
        self.id_person_label = QtGui.QLabel('ID Letter:')

        self.colorBox = QwwColorComboBox()
        for (color_name, color_hex) in CAR_COLORS:
            color = QtGui.QColor(color_hex)
            self.colorBox.addColor(color, color_name)
        #self.id_car_color = QButtonGroup(self)
        #self.id_car_color_buttons = []
        #for color, bg, fg in zip(colorList, bgList, fgList):
        #    newButton = colorSelectButton(text=color, bgcolor=bg, fgcolor=fg)
        #    self.id_car_color.addButton(newButton)
        #    self.id_car_color_buttons.append(newButton)

        self.id_car_number = QtGui.QSpinBox(self)
        self.id_car_number.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)

        self.id_person = QtGui.QComboBox(self)
        self.id_person.addItems(PERSON_LETTERS)

        self.sync_label = QtGui.QLabel('3) Synchronize Image Infromation', self)
        self.sync_number_label = QtGui.QLabel('First Image Number:', self)
        self.sync_time_label = QtGui.QLabel('First Image Timestamp:', self)

        self.sync_number = QtGui.QSpinBox(self)
        self.sync_number.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.sync_time = QtGui.QTimeEdit(self)
        self.sync_time.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)

        self.import_label = QtGui.QLabel('4) Import', self)
        self.import_button = QtGui.QPushButton('Import', self)

    def init_layout(self):
        browse_upper = QtGui.QHBoxLayout()
        browse_upper.addWidget(self.browse_label)
        browse_upper.addWidget(self.browse_button)
        browse_upper.addStretch()

        browse_lower = QtGui.QHBoxLayout()
        browse_lower.addWidget(self.browse_text)
        browse_lower.addStretch()

        browse_group = QtGui.QVBoxLayout()
        browse_group.addLayout(browse_upper)
        browse_group.addLayout(browse_lower)

        id_group = QtGui.QHBoxLayout()
        color_layout = QtGui.QVBoxLayout()
        label_layout = QtGui.QVBoxLayout()
        input_layout = QtGui.QVBoxLayout()
        #for i ,button in enumerate(self.id_car_color_buttons):
        #    id_grid.addWidget(button, i/3, i%3)
        color_layout.addWidget(self.colorBox)
        color_layout.addStretch()

        label_layout.addWidget(self.id_car_label)
        label_layout.addWidget(self.id_person_label)

        input_layout.addWidget(self.id_car_number)
        input_layout.addWidget(self.id_person)

        #id_grid.addWidget(self.colorBox, 0, 1)
        #id_grid.addWidget(self.id_car_label, 0, 2)
        #id_grid.addWidget(self.id_car_number, 0, 3)
        #id_grid.addWidget(self.id_person_label, 1, 2)
        #id_grid.addWidget(self.id_person, 1, 3)

        id_group.addLayout(color_layout)
        id_group.addLayout(label_layout)
        id_group.addLayout(input_layout)
        id_group.addStretch()

        sync_upper = QtGui.QHBoxLayout()
        sync_upper.addWidget(self.sync_number_label)
        sync_upper.addWidget(self.sync_number)
        sync_upper.addStretch()

        sync_lower = QtGui.QHBoxLayout()
        sync_lower.addWidget(self.sync_time_label)
        sync_lower.addWidget(self.sync_time)
        sync_lower.addStretch()

        sync_group = QtGui.QVBoxLayout()
        sync_group.addWidget(self.sync_label)
        sync_group.addLayout(sync_upper)
        sync_group.addLayout(sync_lower)

        import_group = QtGui.QHBoxLayout()
        import_group.addWidget(self.import_label)
        import_group.addWidget(self.import_button)
        import_group.addStretch()

        self.left_hand_layout = QtGui.QVBoxLayout()
        self.left_hand_layout.addWidget(self.logo)
        self.left_hand_layout.addStretch()
        self.left_hand_layout.addLayout(browse_group)
        self.left_hand_layout.addStretch()
        self.left_hand_layout.addWidget(self.id_label)
        self.left_hand_layout.addLayout(id_group)
        self.left_hand_layout.addStretch()
        self.left_hand_layout.addLayout(sync_group)
        self.left_hand_layout.addStretch()
        self.left_hand_layout.addLayout(import_group)

        self.setLayout(self.left_hand_layout)
        self.setFixedWidth(400)

    def init_connect(self):
        self.browse_button.clicked.connect(self.open_directory)
        self.import_button.clicked.connect(self.import_)

    def open_directory(self):
        directory = str(QtGui.QFileDialog.getExistingDirectory(self, 'Select Directory'))
        self.browse_text.setText(directory)

    def import_(self):
        directory = self.browse_text.text()
        files = listdir(directory)
        target_directory = path.join('user_photos', str(self.colorBox.currentText()) + str(self.id_car_number.value()), str(self.id_person.currentText()))
        self.copyThread = CopyThread(directory, files, [target_directory])
        self.connect(self.copyThread, QtCore.SIGNAL('file_done'), self.parent().update_recent_file)
        self.copyThread.start()

    def import_file_list(self, list_):
        # Used for manual import
        directory = path.dirname(str(list_[0]))
        files = [None] * len(list_)
        for i, f in enumerate(list_):
            files[i] = path.basename(str(f))
        target_directory = path.join('user_photos', str(self.colorBox.currentText()) + str(self.id_car_number.value()), str(self.id_person.currentText()))
        self.copyThread = CopyThread(directory, files, [target_directory])
        self.connect(self.copyThread, QtCore.SIGNAL('file_done'), self.parent().update_recent_file)
        self.copyThread.start()


class image_import_interface(QtGui.QWidget):
    def __init__(self, *args):
        apply(QtGui.QWidget.__init__, (self, ) + args)
        QtGui.QWidget.__init__(self)
        self.init_widgets()
        self.init_layout()
        self.init_connect()

    def init_widgets(self):
        self.image_selection_group = selection_group(self)
        self.user_input_group = user_input(self)
        # Hack to get the image_selection_group to fit on the screen

        # self.scroll_area = QtGui.QScrollArea()
        # self.scroll_area.setWidget(self.image_selection_group)
        # self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.scroll_area.setWidgetResizable(True)
        self.progress_bar = QtGui.QLineEdit(self)
        self.submit_button = QtGui.QPushButton('Submit and Upload', self)

    def init_layout(self):
        self.uber_layout = QtGui.QVBoxLayout()
        self.main_layout = QtGui.QHBoxLayout()
        self.main_layout.addWidget(self.user_input_group)
        self.main_layout.addWidget(self.image_selection_group)
        self.uber_layout.addLayout(self.main_layout)
        self.uber_layout.addWidget(self.submit_button)
        self.uber_layout.addWidget(self.progress_bar)

        self.setLayout(self.uber_layout)

    def init_connect(self):
        self.submit_button.clicked.connect(self.submit)

    def submit(self):
        DOMAIN = 'http://localhost:5000/images/submit'
        #Zip selected images: first, last, zebra/, giraffe/
        chdir(path.dirname(path.realpath(__file__)))
        pull_directory = path.join('user_photos', str(self.user_input_group.colorBox.currentText()) + str(self.user_input_group.id_car_number.value()), str(self.user_input_group.id_person.currentText()))
        chdir(path.join(getcwd(), pull_directory))

        first = self.image_selection_group.first_image.current_image
        zebra = []
        giraffe = []
        for IB in self.image_selection_group.image_boxes:
            selection = IB.get_selection()
            if selection[1] == 'Zebra':
                zebra.append(selection[0])
            else:
                giraffe.append(selection[0])

        last = self.image_selection_group.last_image.current_image

        zip_archive = zipfile.ZipFile(str(self.user_input_group.colorBox.currentText()) + str(self.user_input_group.id_car_number.value()) + str(self.user_input_group.id_person.currentText()) + '.zip', 'w')
        zip_archive.write(path.join(getcwd(), first), 'first.jpg')
        zip_archive.write(path.join(getcwd(), last), 'last.jpg')
        for filename in zebra:
            zip_archive.write(path.join(getcwd(), filename), path.join('zebra', filename))
        for filename in giraffe:
            zip_archive.write(path.join(getcwd(), filename), path.join('giraffe', filename))

        zip_archive.close()

        #format data
        data = {
            'car_color': str(self.user_input_group.colorBox.currentText()),
            'car_number': str(self.user_input_group.id_car_number.value()),
            'person_letter': str(self.user_input_group.id_person.currentText()),
            'image_first_time_hour': str(self.user_input_group.sync_time.time().hour()),
            'image_first_time_minute': str(self.user_input_group.sync_time.time().minute()),
        }

        content = open(str(self.user_input_group.colorBox.currentText()) + str(self.user_input_group.id_car_number.value()) + str(self.user_input_group.id_person.currentText()) + '.zip', 'rb')
        files = {
            'image_archive': content,
        }

        # SEND POST REQUEST WITH data AND files PAYLOADS
        r = requests.post(DOMAIN, data=data, files=files)

        # Response
        print('HTTP STATUS:', r.status_code)
        response = json.loads(r.text)
        print('RESPONSE:', response)

    def update_recent_file(self, filename):
        self.progress_bar.setText('Imported new image to ' + filename)
        self.image_selection_group.add_filename(filename)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    win = image_import_interface()
    win.show()
    app.exec_()
    sys.exit()
