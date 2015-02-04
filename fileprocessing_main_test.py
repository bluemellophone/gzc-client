import sys, time, shutil
from PyQt4 import QtCore, QtGui
from fileprocessing_ui_test import Ui_Form
from os import listdir, makedirs, getcwd
from os.path import isfile, join, exists

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
                time.sleep(2)
                shutil.copy2(filepath, outdir)
                self.emit(QtCore.SIGNAL('file_done'), f)
        return


class TestWidget(QtGui.QWidget, Ui_Form):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.connectActions()

    def connectActions(self):
        self.pushButton.clicked.connect(self.openDirectory)
        self.pushButton_2.clicked.connect(self.import_)

    def openDirectory(self):
        directory = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.lineEdit.setText(directory)

    def import_(self):
        directory = self.lineEdit.text()
        files = listdir(directory)        
        self.copyThread = CopyThread(directory, files, ["testfolder"])
        self.connect(self.copyThread, QtCore.SIGNAL("file_done"), self.updateRecent)
        self.copyThread.start()

    def updateRecent(self, filename):
        self.lineEdit_2.setText(filename)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    widget = TestWidget()
    widget.show()
    app.exec_()
