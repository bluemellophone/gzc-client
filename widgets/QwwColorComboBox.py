import PyQt4
from PyQt4 import QtCore, QtGui


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
