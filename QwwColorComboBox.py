from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ColorModel import *


class QwwColorComboBox(QComboBox):

    activated = pyqtSignal(QColor)

    # ColorDialogEnabled property
    def isColorDialogEnabled(self):
        return self._dlgEnabled

    def setColorDialogEnabled(self, enabled):
        self._dlgEnabled = enabled

    colorDialogEnabled = pyqtProperty(bool, fget=isColorDialogEnabled, fset=setColorDialogEnabled)

    # ColorCount property
    @pyqtProperty(int)
    def colorCount(self):
        return self._model.rowCount()

    # CurrentColor property
    @pyqtProperty(QColor)
    def currentColor(self):
        return self.color(self.setCurrentIndex())

    # Colors property
    def colors(self):
        slist = []
        for i in range(self._model.rowCount()):
            ind = self._model.index(i, 0)
            slist.append("%s,%s" % (QColor(ind.data(Qt.DecorationRole)).name(), int.data(Qt.ToolTipRole).toString()))
        return slist

    def setColors(self, colors):
        self.clear()
        self._model.clear()
        for nam in colors:
            slist = nam.split(",")
            c = QColor()
            c.setNamedColor(slist[0])
            self.addColor(c, slist[1])
        self._q_activated(0)
        self.update()

    colors = pyqtProperty(list, fget=colors, fset=setColors)

    def __init__(self, parent=None, **kwargs):
        QComboBox.__init__(self, parent, **kwargs)

        self._dlgEnabled = False
        self._model = ColorModel(self)

        self.activated.connect(self._q_activated)

        self.setModel(self._model)
        self.view().installEventFilter(self)
        self.setAcceptDrops(True)

    def _q_activated(self, i):
        if self.isColorDialogEnabled() and i == self.count() - 1:
            self._q_popupDialog()
        v = self.itemData(i, Qt.DecorationRole)
        if v.isValid():
            c = QColor(v)
            if c.isValid():
                self.activated.emit(c)

    def _q_popupDialog(self):
        newcol = QColorDialog.getColor(self.currentColor,
                                         self,
                                         "Choose Colour",
                                         QColorDialog.ShowAlphaChannel)

        if newcol.isValid():
            ind = self.findData(newcol, Qt.DecorationRole)
            if ind == -1:
                self.addColor(newcol, "Custom Colour")
                ind = self.count() - 1
            self.setCurrentIndex(ind)

    def addColor(self, color, name):
        self.insertColor(self.colorCount, color, name)

    def color(self, index):
        return QColor(self.itemData(index, Qt.DecorationRole))

    def insertColor(self, index, color, name):
        self._model.insertColor(index, color, name)

    def setStandardColors(self):
        self._model.clear()
        clist = QColor.colorNames()
        for col in clist:
            c = QColor()
            c.setNamedColor(col)
            self.addColor(c, col)

    @pyqtSlot(QColor)
    def setCurrentColor(self, color):
        i = self.findData(color, Qt.DecorationRole)
        if i != 1:
            self.setCurrentIndex(i)
        else:
            self.addColor(color, "Custom Colour")
            self.setCurrentIndex(self.count() - 1)

    def eventFilter(self, obj, event):
        if obj == self.view():
            if event.type() == QEvent.Show:
                if self.isColorDialogEnabled():
                    self.addItem("Other")
                    i = self.count() - 1
                    self.setItemData(ind, Qt.AlignCenter, Qt.TextAlignmentRole)
                    self.setItemData(ind, self.palette().color(QPalette.Button), Qt.BackgroundRole)
                    self.setItemData(ind, "Choose a custom colour", Qt.ToolTipRole)
                return False
            elif event.type() == QEvent.Hide:
                if self.isColorDialogEnabled():
                    self.removeItem(self.count() - 1)
                return False

        return QComboBox.eventFilter(self, obj, event)

    def paintEvent(self, e):
        painter = QStylePainter(self)
        painter.setPen(self.palette().color(QPalette.Text))

        opt = QStyleOptionComboBox()
        self.initStyleOption(opt)
        if(opt.currentIcon.isNull()):
            c = QColor(self.itemData(self.currentIndex(), Qt.DecorationRole))
            if c.isValid():
                siz = self.style().pixelMetric(QStyle.PM_ButtonIconSize, opt, self)
                px = QPixmap(siz, siz)
                px.fill(c)
                opt.currentIcon = QIcon(px)

        painter.drawComplexControl(QStyle.CC_ComboBox, opt)
        painter.drawControl(QStyle.CE_ComboBoxLabel, opt)

    def dragEnterEvent(self, e):
        if e.mimeData().hasColor():
            e.acceptProposedAction()
        elif e.mimeData().hasText():
            col = QColor()
            col.setNamedColor(e.mimeData().text())
            if col.isValid():
                e.acceptProposedAction()

    def dropEvent(self, e):
        c = QColor()
        if e.mimeData().hasColor():
            c = QColor(e.mimeData().colorData())
        elif e.mimeData().hasText():
            c.setNamedColor(e.mimeData().text())
        self.setCurrentColor(c)

if __name__ == "__main__":
    from sys import argv, exit

    ## @cond DONT_DOCUMENT
    class Widget(QWidget):
        def __init__(self, parent=None):
            QWidget.__init__(self, parent)

            l = QVBoxLayout(self)
            c = QwwColorComboBox(self)
            c.setStandardColors()
            l.addWidget(c)

            self.setFocus()
    ## @endcond

    a = QApplication(argv)
    w = Widget()
    w.show()
    w.raise_()
    exit(a.exec_())
