from PyQt4.QtCore import *
from PyQt4.QtGui import *

## @cond DONT_DOCUMENT
class ColorModel(QStandardItemModel):
    def __init__(self, parent=None, **kwargs):
        QStandardItemModel.__init__(self, parent, **kwargs)

    def contains(self, color):
        tst=QVariant(color)
        lst=self.match(self.index(0,0), Qt.DecorationRole, tst, 1, Qt.MatchExactly)
        return QModelIndex() if len(lst)==0 else lst[0]

    def clone(self, par=None):
        model=ColorModel(par)
        cnt=self.rowCount()
        for i in range(cnt):
            model.insertRow(i)
            oldData=self.itemData(self.index(i,0))
            model.setItemData(model.index(i,0), oldData)
        return model

    def addColor(self, color, name=""):
        item=QStandardItem()
        item.setText(name)
        item.setData(color, Qt.DecorationRole)
        item.setData(name, Qt.ToolTipRole)
        self.appendRow(item)
        return item.index()

    def insertColor(self, index, color, name=""):
        item=QStandardItem()
        item.setText(name)
        item.setData(color, Qt.DecorationRole)
        self.insertRow(index, item)
        return item.index()
## @endcond  