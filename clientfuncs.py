from __future__ import absolute_import, division, print_function
import shutil
import PyQt4
from PyQt4 import QtCore, QtGui
from os import makedirs
from os.path import isfile, join, exists, splitext, basename
from detecttools.directory import Directory


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class ColorModel(QtGui.QStandardItemModel):
    def __init__(self, parent=None, **kwargs):
        QtGui.QStandardItemModel.__init__(self, parent, **kwargs)

    def contains(self, color):
        tst = QtCore.QVariant(color)
        lst = self.match(self.index(0, 0), QtCore.Qt.DecorationRole, tst, 1, PyQt4.MatchExactly)
        return QtGui.QModelIndex() if len(lst) == 0 else lst[0]

    def clone(self, par=None):
        model = ColorModel(par)
        cnt = self.rowCount()
        for i in range(cnt):
            model.insertRow(i)
            oldData = self.itemData(self.index(i, 0))
            model.setItemData(model.index(i, 0), oldData)
        return model

    def addColor(self, color, name=""):
        item = QtGui.QStandardItem()
        item.setText(name)
        item.setData(color, QtCore.Qt.DecorationRole)
        item.setData(name, PyQt4.ToolTipRole)
        self.appendRow(item)
        return item.index()

    def insertColor(self, index, color, name=""):
        item = QtGui.QStandardItem()
        item.setText(name)
        item.setData(color, QtCore.Qt.DecorationRole)
        self.insertRow(index, item)
        return item.index()


class QwwColorComboBox(QtGui.QComboBox):

    activated = QtCore.pyqtSignal(QtGui.QColor)

    # ColorDialogEnabled property
    def isColorDialogEnabled(self):
        return self._dlgEnabled

    def setColorDialogEnabled(self, enabled):
        self._dlgEnabled = enabled

    colorDialogEnabled = QtCore.pyqtProperty(bool, fget=isColorDialogEnabled, fset=setColorDialogEnabled)

    # ColorCount property
    @QtCore.pyqtProperty(int)
    def colorCount(self):
        return self._model.rowCount()

    # CurrentColor property
    @QtCore.pyqtProperty(QtGui.QColor)
    def currentColor(self):
        return self.color(self.setCurrentIndex())

    # Colors property
    def colors(self):
        slist = []
        for i in range(self._model.rowCount()):
            ind = self._model.index(i, 0)
            slist.append("%s,%s" % (QtGui.QColor(ind.data(QtCore.Qt.DecorationRole)).name(), int.data(PyQt4.ToolTipRole).toString()))
        return slist

    def setColors(self, colors):
        self.clear()
        self._model.clear()
        for nam in colors:
            slist = nam.split(",")
            c = QtGui.QColor()
            c.setNamedColor(slist[0])
            self.addColor(c, slist[1])
        self._q_activated(0)
        self.update()

    colors = QtCore.pyqtProperty(list, fget=colors, fset=setColors)

    def __init__(self, parent=None, **kwargs):
        QtGui.QComboBox.__init__(self, parent, **kwargs)

        self._dlgEnabled = False
        self._model = ColorModel(self)

        self.activated.connect(self._q_activated)

        self.setModel(self._model)
        self.view().installEventFilter(self)
        self.setAcceptDrops(True)

    def _q_activated(self, i):
        if self.isColorDialogEnabled() and i == self.count() - 1:
            self._q_popupDialog()
        v = self.itemData(i, QtCore.Qt.DecorationRole)
        if v.isValid():
            c = QtGui.QColor(v)
            if c.isValid():
                self.activated.emit(c)

    def _q_popupDialog(self):
        newcol = QtGui.QColorDialog.getColor(self.currentColor,
                                             self,
                                             "Choose Colour",
                                             QtGui.QColorDialog.ShowAlphaChannel)

        if newcol.isValid():
            ind = self.findData(newcol, QtCore.Qt.DecorationRole)
            if ind == -1:
                self.addColor(newcol, "Custom Colour")
                ind = self.count() - 1
            self.setCurrentIndex(ind)

    def addColor(self, color, name):
        self.insertColor(self.colorCount, color, name)

    def color(self, index):
        return QtGui.QColor(self.itemData(index, QtCore.Qt.DecorationRole))

    def insertColor(self, index, color, name):
        self._model.insertColor(index, color, name)

    def setStandardColors(self):
        self._model.clear()
        clist = QtGui.QColor.colorNames()
        for col in clist:
            c = QtGui.QColor()
            c.setNamedColor(col)
            self.addColor(c, col)

    @QtCore.pyqtSlot(QtGui.QColor)
    def setCurrentColor(self, color):
        i = self.findData(color, QtCore.Qt.DecorationRole)
        if i != 1:
            self.setCurrentIndex(i)
        else:
            self.addColor(color, "Custom Colour")
            self.setCurrentIndex(self.count() - 1)

    def eventFilter(self, obj, event):
        if obj == self.view():
            if event.type() == QtCore.QEvent.Show:
                if self.isColorDialogEnabled():
                    self.addItem("Other")
                    ind = self.count() - 1
                    self.setItemData(ind, PyQt4.AlignCenter, PyQt4.TextAlignmentRole)
                    self.setItemData(ind, self.palette().color(QtGui.QPalette.Button), PyQt4.BackgroundRole)
                    self.setItemData(ind, "Choose a custom colour", PyQt4.ToolTipRole)
                return False
            elif event.type() == QtCore.QEvent.Hide:
                if self.isColorDialogEnabled():
                    self.removeItem(self.count() - 1)
                return False

        return QtGui.QComboBox.eventFilter(self, obj, event)

    def paintEvent(self, e):
        painter = QtGui.QStylePainter(self)
        painter.setPen(self.palette().color(QtGui.QPalette.Text))

        opt = QtGui.QStyleOptionComboBox()
        self.initStyleOption(opt)
        if(opt.currentIcon.isNull()):
            c = QtGui.QColor(self.itemData(self.currentIndex(), QtCore.Qt.DecorationRole))
            if c.isValid():
                siz = self.style().pixelMetric(QtGui.QStyle.PM_ButtonIconSize, opt, self)
                px = QtGui.QPixmap(siz, siz)
                px.fill(c)
                opt.currentIcon = QtGui.QIcon(px)

        painter.drawComplexControl(QtGui.QStyle.CC_ComboBox, opt)
        painter.drawControl(QtGui.QStyle.CE_ComboBoxLabel, opt)

    def dragEnterEvent(self, e):
        if e.mimeData().hasColor():
            e.acceptProposedAction()
        elif e.mimeData().hasText():
            col = QtGui.QColor()
            col.setNamedColor(e.mimeData().text())
            if col.isValid():
                e.acceptProposedAction()

    def dropEvent(self, e):
        c = QtGui.QColor()
        if e.mimeData().hasColor():
            c = QtGui.QColor(e.mimeData().colorData())
        elif e.mimeData().hasText():
            c.setNamedColor(e.mimeData().text())
        self.setCurrentColor(c)

    def sizeHint(self):
        size = QtGui.QComboBox.sizeHint(self)
        height = size.height()
        width = size.width()
        new_size = QtCore.QSize(width + 20, height)
        return new_size


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(394, 300)
        self.lineEdit = QtGui.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(10, 10, 261, 27))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.lineEdit_2 = QtGui.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(10, 50, 371, 27))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(290, 10, 91, 27))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 90, 371, 27))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.plainTextEdit = QtGui.QPlainTextEdit(Form)
        self.plainTextEdit.setGeometry(QtCore.QRect(10, 130, 371, 151))
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.pushButton.setText(_translate("Form", "Choose Dir", None))
        self.pushButton_2.setText(_translate("Form", "Import", None))


class CopyThread(QtCore.QThread):
    def __init__(self, directory, filenames, destinations):
        QtCore.QThread.__init__(self)
        self.directory = directory
        self.filenames = filenames
        self.destinations = destinations

    def __del__(self):
        self.wait()

    def run(self):
        for f in self.filenames:
            filepath = join(str(self.directory), str(f))
            if not isfile(filepath):
                continue
            for outdir in self.destinations:
                if not exists(outdir):
                    makedirs(outdir)
                # time.sleep(2)
                shutil.copy2(filepath, outdir)
                self.emit(QtCore.SIGNAL('file_done'), (outdir + "/" + f))
        return None


class CoordinateMap:
    """
    Maps coordinates to pixels in an image. Does not account for
    curvature of Earth.
    """
    def __init__(self, ulcoord, brcoord, img):
        img_shape = img.shape
        self.width = img_shape[1]
        self.height = img_shape[0]
        self.ulcoord = ulcoord
        self.brcoord = brcoord
        self.dx, self.dy = self.get_pixel_difference()

    def get_pixel_difference(self):
        # Gets degree / pixel
        import math
        difference_x = math.fabs(self.brcoord[1] - self.ulcoord[1])
        difference_y = math.fabs(self.brcoord[0] - self.ulcoord[0])
        dx = (1.0 * self.width) / difference_x
        dy = (1.0 * self.height) / difference_y
        return dx, dy

    def map_point(self, coord):
        import math
        given_y, given_x = coord
        base_y, base_x = self.ulcoord
        difference_x = math.fabs(given_x - base_x)
        difference_y = math.fabs(given_y - base_y)
        x_loc = int(round((difference_x * self.dx)))
        y_loc = int(round((difference_y * self.dy)))
        if x_loc < 0 or x_loc >= self.width:
            print("Error: point outside image")
            #return (-1, -1)
        if y_loc < 0 or y_loc >= self.height:
            print("Error: point outside image")
            #return (-1, -1)
        return (x_loc, y_loc)

    def map_point_float(self, coord):
        import math
        given_y, given_x = coord
        base_y, base_x = self.ulcoord
        difference_x = math.fabs(given_x - base_x)
        difference_y = math.fabs(given_y - base_y)
        x_loc = (difference_x * self.dx)
        y_loc = (difference_y * self.dy)
        if x_loc < 0 or x_loc >= self.width:
            print("Error: point outside image")
            #return (-1, -1)
        if y_loc < 0 or y_loc >= self.height:
            print("Error: point outside image")
            #return (-1, -1)
        return (x_loc, y_loc)


def find_candidates(search_path, search_str, verbose=True):
    direct = Directory(search_path, recursive=True, include_file_extensions='images')
    transform_list = [
        (lambda x: x),                       # Search for original
        (lambda x: x.lower()),               # Search for lowercase version
        (lambda x: x.upper()),               # Search for uppercase version
        (lambda x: splitext(x)[0]),          # Search without extension
        (lambda x: splitext(x.lower())[0]),  # Search without extension (lowercase)
        (lambda x: splitext(x.upper())[0]),  # Search without extension (uppercase)
        (lambda x: x.replace('.', '')),      # Remove periods
        (lambda x: x.replace('_', '')),      # Remove underscore
        (lambda x: x.replace('-', '')),      # Remove hyphen
        (lambda x: x.replace(' ', '')),      # Remove hyphen
    ]
    found_list = []
    found = False
    for candidate_path in direct.files():
        candidate_str = basename(candidate_path)
        if verbose:
            print("Testing %r" % (candidate_path, ))
        if found:
            if verbose:
                print("    Appending %r" % (candidate_path, ))
            found_list.append(candidate_path)
        else:
            for candidate_transform in transform_list:
                for search_transform in transform_list:
                    candidate_ = candidate_transform(candidate_str)
                    search_    = search_transform(search_str)
                    if candidate_ == search_:
                        if verbose:
                            print("    Trying %r == %r - FOUND!" % (candidate_, search_, ))
                        found = True
                        found_list.append(candidate_path)
                        break
                    else:
                        if verbose:
                            print("    Trying %r == %r" % (candidate_, search_, ))
            else:
                continue
    return found_list


if __name__ == "__main__":
    found = find_candidates('/Users/bluemellophone/Desktop/SD1', 'IMg_1283.jpg')
    print(found)
    print(len(found))

    found = find_candidates('/Users/bluemellophone/Desktop/SD1', 'img_1283.jpg')
    print(found)
    print(len(found))
