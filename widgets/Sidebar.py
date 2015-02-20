import sys
from PyQt4 import QtCore, QtGui
from SidebarSkel import Ui_Sidebar
from ImageFormSkel import Ui_ImageForm
from GPSFormSkel import Ui_GPSForm
from GZCQWidgets import QwwColorComboBox
from os.path import dirname, join
import traceback
from clientfuncs import CopyThread, find_candidates
from os import path

LOGO_SIZE = 200
FILE_DPATH = dirname(__file__)
LOGO_ONE = join(FILE_DPATH, "../assets/logo_ibeis_alpha.png")
LOGO_TWO = join(FILE_DPATH, "../assets/logo_kws_alpha.png")
IMPORT_ICON = join(FILE_DPATH, "../assets/icons/icon_import.png")
BROWSE_ICON = join(FILE_DPATH, "../assets/icons/icon_browse.png")
CLEAR_ICON = join(FILE_DPATH, "../assets/icons/icon_trash.png")

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
CAR_NUMBER = [1, 25]  # [1, 50]
PERSON_LETTERS = ['a', 'b', 'c', 'd', 'e', 'f']  # , 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'aa', 'bb', 'cc', 'dd', 'ee', 'ff', 'gg', 'hh', 'ii', 'jj', 'kk', 'll', 'mm', 'nn', 'oo', 'pp', 'qq', 'rr', 'ss', 'tt', 'uu', 'vv', 'ww', 'xx', 'yy', 'zz']


def ex_deco(action_func):
    #import types
    # import inspect
    #import utool as ut
    # #ut.embed()
    # argspec = inspect.getargspec(action_func)

    def logerr(ex, self=None):
        print ("EXCEPTION RAISED! " + traceback.format_exc(ex))
        log = open('error_log.txt', 'w')
        log.write(traceback.format_exc(ex))
        log.close()
        msg_box = QtGui.QErrorMessage(self)
        msg_box.showMessage(ex.message)
    #is_method = isinstance(action_func, types.MethodType)
    # is_method =  (len(argspec.args) > 0 and argspec.args[0] == 'self')
    def func_wrapper(self, *args):
        # print('+----------<2>')
        # print(action_func)
        # print(argspec)
        # print('self=%r' % (self,))
        # print('args=%r' % (args,))
        # print('L__________')
        try:
            return action_func(self, *args)
        except Exception as ex:
            logerr(ex, self)

    return func_wrapper


class Sidebar(QtGui.QWidget, Ui_Sidebar):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self)
        self.parent = parent
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
        self.submit.setIcon(QtGui.QIcon(IMPORT_ICON))
        self.clear.setIcon(QtGui.QIcon(CLEAR_ICON))
        self.clear.setText("")
        self.imageForm = ImageForm()
        self.gpsForm = GPSForm()
        self.currentForm = 0  # 0 -> imageForm, 1 -> gpsForm
        self.form.addWidget(self.imageForm)
        self.form.addWidget(self.gpsForm)
        self.gpsForm.hide()

    def initConnect(self):
        self.submit.clicked.connect(self.submit_clicked)
        self.clear.clicked.connect(self.clear_clicked)

    def switchWidgets(self, form):
        self.currentForm = form
        if self.currentForm == 0:
            self.imageForm.show()
            self.gpsForm.hide()
        elif self.currentForm == 1:
            self.imageForm.hide()
            self.gpsForm.show()

    # def switchWidgets(self):
    #     self.currentForm = (self.currentForm + 1) % 2
    #     if self.currentForm == 0:
    #         self.imageForm.show()
    #         self.gpsForm.hide()
    #     else:
    #         self.imageForm.hide()
    #         self.gpsForm.show()

    def clear_clicked(self):
        if self.currentForm == 0:
            self.imageForm.clear()
        else:
            self.gpsForm.clear()

    def move_file_list(self, file_list):
        self.parent.img_display.first_image.current_image = file_list.pop(0)
        self.parent.img_display.last_image.current_image = file_list.pop()
        # self.image_selection_group.stored_files = file_list

    def update_recent_file(self, filename):
        #self.progress_bar.setText('Imported new image from ' + filename)
        self.parent.img_display.add_filename(filename)

    def reset_cursor(self):
        QtGui.QApplication.restoreOverrideCursor()

    def submit_clicked(self):
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        print('IMPORT SELF %r' % (self,))
        #print('IMPORT ARGS %r' % (args,))
        directory = str(self.imageForm.drive_display.text())
        print (directory)
        if directory == "":
            raise IOError("Please select the directory that contains the photos you wish to import from.")
            return
        if str(self.imageForm.name_input.text()) == "":
            raise IOError("The first image name must be defined.")
            return
        self.files = find_candidates(directory, str(self.imageForm.name_input.text()))
        if len(self.files) == 0:
            raise IOError("Could not find any files for selected directory. Please check your first image name.")
            return
        #send this file list to the selection group i am a bad programmer
        self.file_bases = [path.basename(f) for f in self.files]
        print self.file_bases
        self.move_file_list(self.file_bases)

        target_directory = path.join('..', 'data', 'images', str(self.imageForm.color_input.currentText()) + str(self.imageForm.number_input.value()), str(self.imageForm.letter_input.currentText()))
        self.copyThread = CopyThread(self.files, [target_directory])
        self.connect(self.copyThread, QtCore.SIGNAL('file_done'), self.update_recent_file)
        self.connect(self.copyThread, QtCore.SIGNAL('completed'), self.reset_cursor)
        self.copyThread.start()


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
        self.drive_browse.setIcon(QtGui.QIcon(BROWSE_ICON))

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
