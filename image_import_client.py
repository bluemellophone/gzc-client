from PyQt4.QtGui import *
from PyQt4.QtCore import *
from gpsclient import colorSelectButton
import sys
import platform

#TODO: 
# framework to avoid re-use of already observed images
# parallel import
# add status bar to bottom

class image_selection_roll(QLabel):
    #Need to modify the QLabel functionality to allow it to act like a button 
    DEFAULT_IMAGE = 'reroll.png'

    def __init__(self, parent):
        QLabel.__init__(self, parent)
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
        self.connect(self.image, SIGNAL('clicked()'), lambda: self.reroll(self.image))


    def reroll(self, image_button):
        image_button.changeImage("test/first.jpg")
        #uncheck the buttons if image is rerolled
        checked = self.select_group.checkedButton()
        print checked
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


class user_input(QWidget):
    def __init__(self, *args):
        apply(QWidget.__init__,(self, ) + args)
        QWidget.__init__(self)
        self.init_widgets()
        self.init_layout()
        # self.init_connect()

    def init_widgets(self):
        self.browse_label = QLabel("1) Select Drive With SD card:", self)
        self.browse_button = QPushButton("Browse", self)
        self.browse_text = QLineEdit(self)


        self.id_label = QLabel("2) Input Identification Information", self)
        self.id_car_label = QLabel("Car Number:", self)
        self.id_person_label = QLabel("ID Letter:")

        colorList = ["Red", "Green", "Blue", "Yellow", "Black", "White"]
        bgList = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 0, 0), (255, 255, 255)]
        fgList = [(255, 255, 255), (255, 255, 255), (255, 255, 255), None, (255, 255, 255), None, None]
        self.id_car_color = QButtonGroup(self)
        self.id_car_color_buttons = []
        for color, bg, fg in zip(colorList, bgList, fgList):
            newButton = colorSelectButton(text=color, bgcolor=bg, fgcolor=fg)
            self.id_car_color.addButton(newButton)
            self.id_car_color_buttons.append(newButton)

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

        browse_lower = QHBoxLayout()
        browse_lower.addStretch()
        browse_lower.addWidget(self.browse_text)

        browse_group = QVBoxLayout()
        browse_group.addLayout(browse_upper)
        browse_group.addLayout(browse_lower)

        id_grid = QGridLayout()
        for i ,button in enumerate(self.id_car_color_buttons):
            id_grid.addWidget(button, i/3, i%3)
        id_grid.addWidget(self.id_car_label, 0, 3)
        id_grid.addWidget(self.id_car_number, 0, 4)
        id_grid.addWidget(self.id_person_label, 1, 3)
        id_grid.addWidget(self.id_person_text, 1, 4)

        id_group = QVBoxLayout()
        id_group.addWidget(self.id_label)
        id_group.addLayout(id_grid)

        sync_upper = QHBoxLayout()
        sync_upper.addWidget(self.sync_number_label)
        sync_upper.addWidget(self.sync_number)

        sync_lower = QHBoxLayout()
        sync_lower.addWidget(self.sync_time_label)
        sync_lower.addWidget(self.sync_time)

        sync_group = QVBoxLayout()
        sync_group.addWidget(self.sync_label)
        sync_group.addLayout(sync_upper)
        sync_group.addLayout(sync_lower)

        import_group = QHBoxLayout()
        import_group.addWidget(self.import_label)
        import_group.addWidget(self.import_button)


        self.left_hand_layout = QVBoxLayout()
        self.left_hand_layout.addLayout(browse_group)
        self.left_hand_layout.addStretch()
        self.left_hand_layout.addLayout(id_group)
        self.left_hand_layout.addStretch()
        self.left_hand_layout.addLayout(sync_group)
        self.left_hand_layout.addStretch()
        self.left_hand_layout.addLayout(import_group)

        self.setLayout(self.left_hand_layout)


class image_import_interface(QWidget):
    def __init__(self, *args):
        apply(QWidget.__init__,(self, ) + args)
        QWidget.__init__(self)
        self.init_widgets()
        self.init_layout()

    def init_widgets(self):
        self.image_selection_group = selection_group(self)
        self.user_input_group = user_input(self)

    def init_layout(self):
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.user_input_group)
        self.main_layout.addWidget(self.image_selection_group)

        self.setLayout(self.main_layout)



        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = image_import_interface()
    win.show()
    app.exec_()
    sys.exit()