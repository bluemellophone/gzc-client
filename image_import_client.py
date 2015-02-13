from PyQt4.QtGui import *
from PyQt4.QtCore import *
from fileprocessing_main_test import CopyThread
from os import listdir, makedirs, getcwd
import random
import sys
import platform
import copy
from QwwColorComboBox import QwwColorComboBox

#TODO: 
# add status bar to bottom -- WIP

class image_selection_roll(QLabel):
    #Modify the QLabel functionality to allow it to act like a button 
    DEFAULT_IMAGE = 'reroll.png'

    def __init__(self, *args):
        apply(QLabel.__init__,(self, ) + args)
        QLabel.__init__(self)
        self.setScaledContents(True)
        Pixmap = QPixmap((self.DEFAULT_IMAGE)).scaled(QSize(150,150))
        self.desiredsize = Pixmap.size();
        self.setPixmap(Pixmap)
        self.current_image =  self.DEFAULT_IMAGE
 
    def mouseReleaseEvent(self, ev):
        self.emit(SIGNAL('clicked()'))

    def changeImage(self, image_file):
        self.setPixmap(QPixmap(image_file).scaled(self.desiredsize));
        self.current_image = image_file


class image_selection_box(QWidget):
    #One selection box. Contains the image and two buttons
    def __init__(self, *args):
        apply(QWidget.__init__,(self, ) + args)
        QWidget.__init__(self)

        self.init_widgets()
        self.init_layout()
        self.init_connect()

    def init_widgets(self):
        self.image = image_selection_roll(self)
        self.select_zebra = QRadioButton('Zebra',self)
        self.select_giraffe = QRadioButton('Giraffe',self)

        self.select_group = QButtonGroup(self)
        self.select_group.addButton(self.select_zebra)
        self.select_group.addButton(self.select_giraffe)


    def init_layout(self):
        grid = QGridLayout()
        grid.addWidget(self.image, 0, 0, 1, 0)
        grid.addWidget(self.select_zebra, 2, 0)
        grid.addWidget(self.select_giraffe, 2, 1)

        self.setLayout(grid)

    def init_connect(self):
        self.connect(self.image, SIGNAL('clicked()'), self.reroll)


    def reroll(self):
        #get new filename
        filename = self.parent().get_filename()

        self.image.changeImage(filename)
        #uncheck the buttons if image is rerolled
        checked = self.select_group.checkedButton()
        # print checked
        if checked is not None:
            #HACK to reset all checked states
            self.select_group.setExclusive(False)
            checked.setChecked(False)
            self.select_group.setExclusive(True)

    def get_selection(self):
        return (self.image.current_image, self.selection_group.checkedButton())

class selection_group(QWidget):
    #The right side of the interface
    def __init__(self, *args):
        apply(QWidget.__init__,(self, ) + args)
        QWidget.__init__(self)
        self.init_widgets()
        self.init_layout()
        self.stored_files = []
        self.active_files = []
        # self.init_connect()

    def init_widgets(self):
        self.image_boxes = []
        for i in range(12):
            self.image_boxes.append(image_selection_box(self))

    def init_layout(self):
        grid = QGridLayout()
        for i, image_box in enumerate(self.image_boxes):
            grid.addWidget(image_box, i/3, i%3)

        self.setLayout(grid)

    def add_filename(self, filename):
        self.active_files.append(filename)
        self.stored_files.append(filename)
        #for the first couple of images to be copied, we will update the displayed photos
        if len(self.active_files) < 2:
            for IB in self.image_boxes:
                if IB.image.current_image == IB.image.DEFAULT_IMAGE:
                    IB.reroll()
                    break

    def get_filename(self):
        if len(self.active_files) ==  0:
            # If we've run through all the filename, just blindly restart the q
            self.active_files = copy.deepcopy(self.stored_files)

        filename = self.active_files.pop((random.randrange(len(self.active_files))))
        return filename




class user_input(QWidget):
    def __init__(self, *args):
        apply(QWidget.__init__,(self, ) + args)
        QWidget.__init__(self)
        self.init_widgets()
        self.init_layout()
        self.init_connect()

    def init_widgets(self):
        self.logo = QLabel(self)
        self.logo.setPixmap(QPixmap("ibeis_logo.png").scaled(QSize(100,100)))

        self.browse_label = QLabel("1) Select Drive With SD card:", self)
        self.browse_button = QPushButton("Browse", self)
        self.browse_text = QLineEdit(self)


        self.id_label = QLabel("2) Input Identification Information", self)
        self.id_car_label = QLabel("Car Number:", self)
        self.id_person_label = QLabel("ID Letter:")

        self.colorList = ["Red", "Green", "Blue", "Yellow", "Black", "White"]
        bgList = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 0, 0), (255, 255, 255)]
        self.colorBox = QwwColorComboBox()
        for color_name, rgb in zip(self.colorList, bgList):
            color = QColor(rgb[0], rgb[1], rgb[2])
            self.colorBox.addColor(color, color_name)
        #self.id_car_color = QButtonGroup(self)
        #self.id_car_color_buttons = []
        #for color, bg, fg in zip(colorList, bgList, fgList):
        #    newButton = colorSelectButton(text=color, bgcolor=bg, fgcolor=fg)
        #    self.id_car_color.addButton(newButton)
        #    self.id_car_color_buttons.append(newButton)

        self.id_car_number = QSpinBox(self)
        self.id_car_number.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.id_person_text = QLineEdit(self)

        self.sync_label = QLabel("3) Synchronize Image Infromation", self)
        self.sync_number_label = QLabel("First Image Number:", self)
        self.sync_time_label = QLabel("First Image Timestamp:", self)

        self.sync_number = QSpinBox(self)
        self.sync_number.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.sync_time = QTimeEdit(self)
        self.sync_time.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.import_label = QLabel("4) Import", self)
        self.import_button = QPushButton("Import", self)


    def init_layout(self):
        browse_upper = QHBoxLayout()
        browse_upper.addWidget(self.browse_label)
        browse_upper.addWidget(self.browse_button)
        browse_upper.addStretch()

        browse_lower = QHBoxLayout()
        browse_lower.addWidget(self.browse_text)
        browse_lower.addStretch()

        browse_group = QVBoxLayout()
        browse_group.addLayout(browse_upper)
        browse_group.addLayout(browse_lower)

        id_group = QHBoxLayout()
        color_layout = QVBoxLayout()
        label_layout = QVBoxLayout()
        input_layout = QVBoxLayout()
        #for i ,button in enumerate(self.id_car_color_buttons):
        #    id_grid.addWidget(button, i/3, i%3)
        color_layout.addWidget(self.colorBox)
        color_layout.addStretch()

        label_layout.addWidget(self.id_car_label)
        label_layout.addWidget(self.id_person_label)

        input_layout.addWidget(self.id_car_number)
        input_layout.addWidget(self.id_person_text)

        #id_grid.addWidget(self.colorBox, 0, 1)
        #id_grid.addWidget(self.id_car_label, 0, 2)
        #id_grid.addWidget(self.id_car_number, 0, 3)
        #id_grid.addWidget(self.id_person_label, 1, 2)
        #id_grid.addWidget(self.id_person_text, 1, 3)

        id_group.addLayout(color_layout)
        id_group.addLayout(label_layout)
        id_group.addLayout(input_layout)
        id_group.addStretch()

        sync_upper = QHBoxLayout()
        sync_upper.addWidget(self.sync_number_label)
        sync_upper.addWidget(self.sync_number)
        sync_upper.addStretch()

        sync_lower = QHBoxLayout()
        sync_lower.addWidget(self.sync_time_label)
        sync_lower.addWidget(self.sync_time)
        sync_lower.addStretch()

        sync_group = QVBoxLayout()
        sync_group.addWidget(self.sync_label)
        sync_group.addLayout(sync_upper)
        sync_group.addLayout(sync_lower)

        import_group = QHBoxLayout()
        import_group.addWidget(self.import_label)
        import_group.addWidget(self.import_button)
        import_group.addStretch()


        self.left_hand_layout = QVBoxLayout()
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

    def init_connect(self):
        self.browse_button.clicked.connect(self.open_directory)
        self.import_button.clicked.connect(self.import_)


    def open_directory(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.browse_text.setText(directory)

    def import_(self):
        directory = self.browse_text.text()
        files = listdir(directory)        
        self.copyThread = CopyThread(directory, files, ["testfolder"])
        self.connect(self.copyThread, SIGNAL("file_done"), self.parent().update_recent_file)
        self.copyThread.start()

class image_import_interface(QWidget):
    def __init__(self, *args):
        apply(QWidget.__init__,(self, ) + args)
        QWidget.__init__(self)
        self.init_widgets()
        self.init_layout()

    def init_widgets(self):
        self.image_selection_group = selection_group(self)
        self.user_input_group = user_input(self)
        #self.scroll_area = QScrollArea()
        #self.scroll_area.setWidget(self.image_selection_group)
        #self.scroll_area.setHorizontalScrollBarPolicy(1)
        self.progress_bar = QLineEdit(self)

    def init_layout(self):
        self.uber_layout = QVBoxLayout()
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.user_input_group)
        self.main_layout.addWidget(self.image_selection_group)
        #self.main_layout.addWidget(self.scroll_area)
        self.uber_layout.addLayout(self.main_layout)
        self.uber_layout.addWidget(self.progress_bar)

        self.setLayout(self.uber_layout)

    def update_recent_file(self, filename):
        self.progress_bar.setText("Imported new image to " + filename)
        self.image_selection_group.add_filename(filename)



        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = image_import_interface()
    win.show()
    app.exec_()
    sys.exit()
