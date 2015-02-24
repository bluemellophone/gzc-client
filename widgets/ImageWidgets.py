from __future__ import absolute_import, division, print_function
from PyQt4 import QtCore, QtGui
from clientfuncs import resource_path
from os import path
import time
import random
import copy


PLACEHOLDER_IMAGE = resource_path('assets/placeholder.png')
ZEBRA_ICON        = resource_path('assets/icons/icon_zebra.png')
GIRAFFE_ICON      = resource_path('assets/icons/icon_giraffe.png')


class image_selection_roll_first_last(QtGui.QLabel):
    #Modify the QtGui.QLabel functionality to allow it to act like a button
    def __init__(self, *args):
        QtGui.QLabel.__init__(self)
        self.init_layout()

    def init_layout(self):
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        self.clear()

    def get_timestamp(self):
        if self.current_image == PLACEHOLDER_IMAGE:
            return 'Awaiting images...'
        else:
            return time.strftime('%d/%m/%y, %H:%M:%S', time.gmtime(path.getmtime(self.current_image)))

    def triggerResize(self):
        self.clear(self.current_image, reuse=False)

    def clear(self, filename=None, reuse=False):
        if filename is None:
            filename = PLACEHOLDER_IMAGE
        if reuse:
            Pixmap = self.pixmap()
        else:
            Pixmap = QtGui.QPixmap(filename)
        self.current_image = filename
        print(self.size())
        Pixmap = Pixmap.scaled(self.size(), QtCore.Qt.KeepAspectRatio)
        self.setPixmap(Pixmap)


class image_selection_box_first_last(QtGui.QWidget):
    #One selection box. Contains the image and two buttons
    def __init__(self, *args):
        QtGui.QWidget.__init__(self)
        self.init_widgets()
        self.init_layout()
        self.init_visual()

    def init_widgets(self):
        self.image = image_selection_roll(self)
        self.image_time = QtGui.QLabel(self.image.get_timestamp(), self)
        self.image_time.setAlignment(QtCore.Qt.AlignCenter)
        self.info_text = QtGui.QLabel(parent=self)
        self.info_text.setAlignment(QtCore.Qt.AlignCenter)
        self.info_text.setMinimumHeight(25)

    def init_layout(self):
        grid = QtGui.QGridLayout()
        grid.addWidget(self.image, 0, 0, 1, 0)
        grid.addWidget(self.image_time, 2, 0, 1, 0)
        grid.addWidget(self.info_text, 3, 0, 1, 0)
        self.setLayout(grid)
        self.clear()

    def init_visual(self):
        # self.setStyleSheet('background-color: red;')
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QtGui.QColor("#e2e2e2"))
        self.setPalette(p)

    def update(self, filename):
        self.image.clear(filename)

    def triggerResize(self):
        self.image.triggerResize()

    def clear(self):
        self.image.clear()
        self.image_time.setText('Awaiting images...')


class image_selection_roll(QtGui.QLabel):
    #Modify the QtGui.QLabel functionality to allow it to act like a button
    def __init__(self, *args):
        QtGui.QLabel.__init__(self)
        self.init_layout()

    def init_layout(self):
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        self.clear()

    def mouseReleaseEvent(self, ev):
        if self.current_image != PLACEHOLDER_IMAGE:
            self.emit(QtCore.SIGNAL('clicked()'))

    def enterEvent(self, ev):
        if self.current_image != PLACEHOLDER_IMAGE:
            QtGui.QApplication.setOverrideCursor(QtCore.Qt.PointingHandCursor)

    def leaveEvent(self, event):
        if self.current_image != PLACEHOLDER_IMAGE:
            QtGui.QApplication.restoreOverrideCursor()

    def changeImage(self, image_file):
        self.clear(image_file)

    def get_timestamp(self):
        if self.current_image == PLACEHOLDER_IMAGE:
            return 'Awaiting images...'
        else:
            return time.strftime('%d/%m/%y, %H:%M:%S', time.gmtime(path.getmtime(self.current_image)))

    def triggerResize(self):
        self.clear(self.current_image, reuse=False)

    def clear(self, filename=None, reuse=False):
        if filename is None:
            filename = PLACEHOLDER_IMAGE
        if reuse:
            Pixmap = self.pixmap()
        else:
            Pixmap = QtGui.QPixmap(filename)
        self.current_image = filename
        Pixmap = Pixmap.scaled(self.size(), QtCore.Qt.KeepAspectRatio)
        self.setPixmap(Pixmap)


class image_selection_box(QtGui.QWidget):
    #One selection box. Contains the image and two buttons
    def __init__(self, *args):
        QtGui.QWidget.__init__(self)
        self.init_widgets()
        self.init_layout()
        self.init_connect()

    def init_widgets(self):
        self.image = image_selection_roll(self)
        self.select_zebra = QtGui.QPushButton('Zebra', self)
        self.select_zebra.setIcon(QtGui.QIcon(ZEBRA_ICON))
        self.select_giraffe = QtGui.QPushButton('Giraffe', self)
        self.select_giraffe.setIcon(QtGui.QIcon(GIRAFFE_ICON))
        self.select_zebra.setCheckable(True)
        self.select_zebra.setEnabled(False)
        self.select_giraffe.setCheckable(True)
        self.select_giraffe.setEnabled(False)

        self.select_group = QtGui.QButtonGroup(self)
        self.select_group.addButton(self.select_zebra)
        self.select_group.addButton(self.select_giraffe)

        self.image_time = QtGui.QLabel(self.image.get_timestamp(), self)
        self.image_time.setAlignment(QtCore.Qt.AlignCenter)

    def init_layout(self):
        grid = QtGui.QGridLayout()
        grid.addWidget(self.image, 0, 0, 1, 0)
        grid.addWidget(self.image_time, 2, 0, 1, 0)
        grid.addWidget(self.select_zebra, 3, 0)
        grid.addWidget(self.select_giraffe, 3, 1)
        self.setLayout(grid)
        self.clear()

    def init_connect(self):
        self.connect(self.image, QtCore.SIGNAL('clicked()'), self.reroll)
        self.select_group.buttonClicked[int].connect(self.option_selected)

    def reroll(self, filename=None):
        #get new filename
        try:
            if filename is None:
                filename = self.parent().get_filename()
        except ValueError:
            return
        self.image.changeImage(filename)
        self.image_time.setText(self.image.get_timestamp())
        self.select_zebra.setEnabled(True)
        self.select_giraffe.setEnabled(True)
        #uncheck the buttons if image is rerolled
        checked = self.select_group.checkedButton()
        # print checked
        if checked is not None:
            #HACK to reset all checked states
            self.select_group.setExclusive(False)
            checked.setChecked(False)
            self.select_group.setExclusive(True)
        self.emit(QtCore.SIGNAL('images_modified'))

    def option_selected(self):
        self.emit(QtCore.SIGNAL('images_modified'))

    def is_selected(self):
        enabled = self.select_zebra.isEnabled() and self.select_giraffe.isEnabled()
        return not enabled or int(self.select_group.checkedId()) != -1

    def get_selection(self):
        enabled = self.select_zebra.isEnabled() and self.select_giraffe.isEnabled()
        if not enabled:
            return (None, 'Ignore')
        checked = self.select_group.checkedButton()
        if checked is None:
            return (None, 'Unassigned')
        return (path.basename(self.image.current_image), checked.text())

    def triggerResize(self):
        self.image.triggerResize()

    def clear(self):
        self.image.clear()
        self.image_time.setText('Awaiting images...')
        self.select_zebra.setEnabled(False)
        self.select_giraffe.setEnabled(False)
        checked = self.select_group.checkedButton()
        if checked is not None:
            #HACK to reset all checked states
            self.select_group.setExclusive(False)
            checked.setChecked(False)
            self.select_group.setExclusive(True)


class selection_group(QtGui.QWidget):
    #The right side of the interface
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        self.init_widgets()
        self.init_layout()
        self.stored_files = []
        self.active_files = []
        # self.init_connect()

    def init_widgets(self):
        self.first_image = image_selection_box_first_last(self)
        self.first_image.info_text.setText('First Image in Directory')
        self.image_boxes = []
        for i in range(10):
            box = image_selection_box(self)
            self.image_boxes.append(box)
            self.connect(box, QtCore.SIGNAL('images_modified'), self.images_modified)

        self.last_image = image_selection_box_first_last(self)
        self.last_image.info_text.setText('Last Image in Directory')

    def all_images_selected(self):
        for image_box in self.image_boxes:
            if not image_box.is_selected():
                return False
        return True

    def images_modified(self):
        self.emit(QtCore.SIGNAL('images_modified'))

    def init_layout(self):

        gridV = QtGui.QVBoxLayout()
        hor1 = QtGui.QHBoxLayout()
        hor2 = QtGui.QHBoxLayout()
        hor3 = QtGui.QHBoxLayout()
        # hor1.addStretch(1)
        hor1.addWidget(self.first_image)
        # hor1.addStretch(1)
        hor1.addWidget(self.image_boxes[0])
        # hor1.addStretch(1)
        hor1.addWidget(self.image_boxes[1])
        # hor1.addStretch(1)
        hor1.addWidget(self.image_boxes[2])
        # hor1.addStretch(1)
        # hor2.addStretch(1)
        hor2.addWidget(self.image_boxes[3])
        # hor2.addStretch(1)
        hor2.addWidget(self.image_boxes[4])
        # hor2.addStretch(1)
        hor2.addWidget(self.image_boxes[5])
        # hor2.addStretch(1)
        hor2.addWidget(self.image_boxes[6])
        # hor2.addStretch(1)
        # hor3.addStretch(1)
        hor3.addWidget(self.image_boxes[7])
        # hor3.addStretch(1)
        hor3.addWidget(self.image_boxes[8])
        # hor3.addStretch(1)
        hor3.addWidget(self.image_boxes[9])
        # hor3.addStretch(1)
        hor3.addWidget(self.last_image)
        # hor3.addStretch(1)
        # gridV.addStretch(1)
        gridV.addLayout(hor1)
        # gridV.addStretch(1)
        gridV.addLayout(hor2)
        # gridV.addStretch(1)
        gridV.addLayout(hor3)
        # gridV.addStretch(1)

        self.setLayout(gridV)

    def add_filename(self, filename, add_to_display):
        # self.active_files.append(filename)
        # self.stored_files.append(filename)
        #for the first couple of images to be copied, we will update the displayed photos
        if path.basename(filename) == self.first_image.current_image:
            #FIRST IMAGE, add to the first image box
            self.first_image.update(filename)
        elif path.basename(filename) == self.last_image.current_image:
            self.last_image.update(filename)
        else:
            self.active_files.append(filename)
            self.stored_files.append(filename)
            if add_to_display:
                for IB in self.image_boxes:
                    if IB.image.current_image == PLACEHOLDER_IMAGE:
                            IB.reroll(filename)
                            break
        #if we've filled the image boxes, update the last image

    def clear(self):
        self.stored_files = []
        self.active_files = []
        self.first_image.clear()
        self.last_image.clear()
        for image_box in self.image_boxes:
            image_box.clear()

    def triggerResize(self):
        self.first_image.triggerResize()
        self.last_image.triggerResize()
        for image_box in self.image_boxes:
            image_box.triggerResize()

    def get_filename(self):
        if len(self.active_files) ==  0:
            # If we've run through all the filename, just blindly restart the q
            self.active_files = copy.deepcopy(self.stored_files)
            for IB in self.image_boxes:
                self.active_files.remove(IB.image.current_image)
        filename = self.active_files.pop((random.randrange(len(self.active_files))))
        return filename
