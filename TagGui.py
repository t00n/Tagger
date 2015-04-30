from PyQt4 import QtGui, QtCore
import sys

from Config import Config
from Collection import Collection
import MainWindowUI

class TagGuiWindow(QtGui.QMainWindow, MainWindowUI.Ui_MainWindow):
    def __init__(self, config, parent=None):
        super(TagGuiWindow, self).__init__(parent)
        self.setupUi(self)
        self.actionOpen.triggered.connect(self.openCollection)
        self.actionScan.triggered.connect(self.scanCollection)
        self.actionSave.triggered.connect(self.saveCollection)
        self.actionExit.triggered.connect(self.close)

        self.actionAdd_tags.triggered.connect(self.addTags)
        self.actionRemove_tags.triggered.connect(self.removeTags)

        
    def keyPressEvent(self, event):
        """ """
        if event.key() == QtCore.Qt.Key_Left or event.key() == QtCore.Qt.Key_Escape:
            self.prevImage()
        elif event.key() == QtCore.Qt.Key_Right:
            self.nextImage()

    def prevImage(self):
        index = self.stackedWidget.currentIndex() - 1
        if index < 0:
            index = self.stackedWidget.count() - 1
        self.stackedWidget.setCurrentIndex(index)

    def nextImage(self):
        index = self.stackedWidget.currentIndex() + 1
        if index >= self.stackedWidget.count():
            index = 0
        self.stackedWidget.setCurrentIndex(index)


    def openCollection(self):
        dir = QtGui.QFileDialog.getExistingDirectory()
        if dir != "":
            self.collection = Collection(dir)
            for image in self.collection.images.itervalues():
                label = QtGui.QLabel()
                pixmap = QtGui.QPixmap(image.location)
                label.setPixmap(pixmap)
                # label.setText(image.location)
                self.stackedWidget.addWidget(label)

    def scanCollection(self):
        if self.collection:
            self.collection.scan()

    def saveCollection(self):
        if self.collection:
            self.collection.save()

    def addTags(self):
        pass

    def removeTags(self):
        pass

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    config = Config()
    window = TagGuiWindow(config)
    window.show()
    app.exec_()