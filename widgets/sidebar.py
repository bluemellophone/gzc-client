import sys
from PyQt4 import QtCore, QtGui
from SidebarSkel import Ui_Sidebar
from ImageFormSkel import Ui_ImageForm
from GPSFormSkel import Ui_GPSForm
from QwwColorComboBox import QwwColorComboBox
from os.path import dirname, join

LOGO_SIZE = 200
FILE_DPATH = dirname(__file__)
LOGO_ONE = join(FILE_DPATH, "../assets/logo.png")
LOGO_TWO = join(FILE_DPATH, "../assets/logo.png")

CAR_COLORS = [
    ('white',    '#FFFFFF'),
    ('red',        '#D9534F'),
    ('orange', '#EF7A4C'),
    ('yellow', '#F0AD4E'),
    ('green',    '#5CB85C'),
    ('blue',     '#3071A9'),
    ('purple', '#6F5499'),
    ('black',    '#333333'),
]
CAR_NUMBER = [1, 50]
PERSON_LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'aa', 'bb', 'cc', 'dd', 'ee', 'ff', 'gg', 'hh', 'ii', 'jj', 'kk', 'll', 'mm', 'nn', 'oo', 'pp', 'qq', 'rr', 'ss', 'tt', 'uu', 'vv', 'ww', 'xx', 'yy', 'zz']


class Sidebar(QtGui.QWidget, Ui_Sidebar):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.initLogos()
        self.initWidgets()
        self.initConnect()

    def initLogos(self):
        logo1 = QtGui.QPixmap(LOGO_ONE).scaled(QtCore.QSize(LOGO_SIZE, LOGO_SIZE), QtCore.Qt.KeepAspectRatio)
        logo2 = QtGui.QPixmap(LOGO_TWO).scaled(QtCore.QSize(LOGO_SIZE, LOGO_SIZE), QtCore.Qt.KeepAspectRatio)
        self.logo_1.setPixmap(logo1)
        self.logo_2.setPixmap(logo2)

    def initWidgets(self):
        self.imageForm = ImageForm()
        self.gpsForm = GPSForm()
        self.currentForm = 0  # 0 -> imageForm, 1 -> gpsForm
        self.form.addWidget(self.imageForm)
        self.form.addWidget(self.gpsForm)
        self.gpsForm.hide()

    def initConnect(self):
        self.submit.clicked.connect(self.submit_clicked)
        self.clear.clicked.connect(self.clear_clicked)

    def switchWidgets(self):
        self.currentForm = (self.currentForm + 1) % 2
        if self.currentForm == 0:
            self.imageForm.show()
            self.gpsForm.hide()
        else:
            self.imageForm.hide()
            self.gpsForm.show()

    def clear_clicked(self):
        if self.currentForm == 0:
            self.imageForm.clear()
        else:
            self.gpsForm.clear()

    def submit_clicked(self):
        pass


class ImageForm(QtGui.QWidget, Ui_ImageForm):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.initWidgets()
        self.initConnect()

    def initWidgets(self):
        self.drive_display.setReadOnly(True)
        self.number_input.setMinimum(CAR_NUMBER[0])
        self.number_input.setMaximum(CAR_NUMBER[1])
        self.letter_input.addItems(PERSON_LETTERS)
        self.color_input = QwwColorComboBox()
        self.color_input_space.addWidget(self.color_input)
        for (color_name, color_hex) in CAR_COLORS:
            color = QtGui.QColor(color_hex)
            self.color_input.addColor(color, color_name)

    def initConnect(self):
        self.drive_browse.clicked.connect(self.open_directory)

    def open_directory(self):
        directory = str(QtGui.QFileDialog.getExistingDirectory(self, 'Select Directory'))
        self.drive_display.setText(directory)

    def clear(self):
        self.drive_display.setText("")
        self.color_input.setCurrentIndex(0)
        self.number_input.setValue(1)
        self.letter_input.setCurrentIndex(0)
        self.name_input.setText("")
        self.time_input.setTime(QtCore.QTime(0, 0, 0, 0))


class GPSForm(QtGui.QWidget, Ui_GPSForm):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.initWidgets()

    def initWidgets(self):
        self.color_input = QwwColorComboBox()
        self.color_input_space.addWidget(self.color_input)
        self.number_input.setMinimum(CAR_NUMBER[0])
        self.number_input.setMaximum(CAR_NUMBER[1])
        for (color_name, color_hex) in CAR_COLORS:
            color = QtGui.QColor(color_hex)
            self.color_input.addColor(color, color_name)

    def clear(self):
        self.color_input.setCurrentIndex(0)
        self.number_input.setValue(1)
        self.time_input.setTime(QtCore.QTime(0, 0, 0, 0))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    widget = Sidebar()
    widget.show()
    sys.exit(app.exec_())
