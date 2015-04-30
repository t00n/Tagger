from PyQt4 import QtGui, QtCore
import sys

from Config import Config
from Collection import Collection
import MainWindowUI

class TagGuiWindow(QtGui.QMainWindow, MainWindowUI.Ui_MainWindow):
    WINDOW_TITLE = "TagGui"
    def __init__(self, config, parent=None):
        super(TagGuiWindow, self).__init__(parent)
        self.setupUi(self)
        self.actionOpen.triggered.connect(self._openCollection)
        self.actionScan.triggered.connect(self._scanCollection)
        self.actionSave.triggered.connect(self._saveCollection)
        self.actionExit.triggered.connect(self.close)

        self.queryEdit.returnPressed.connect(self._queryCollection)

        self.collection = None
        self.currentImages = []

    def keyPressEvent(self, event):
        """ """
        if event.key() == QtCore.Qt.Key_Left:
            self._prevImage()
        elif event.key() == QtCore.Qt.Key_Right:
            self._nextImage()
        elif event.key() == QtCore.Qt.Key_Escape:
            self.setFocus()

    def mousePressEvent(self, event):
        # TODO zoom in/out
        pass

    def _selectImage(self, index):
        self.stackedWidget.setCurrentIndex(index)
        if 0 <= index < len(self.currentImages):
            self.setWindowTitle(self.WINDOW_TITLE + " - " + self.currentImages[index].location)
            # tags
            tags = ""
            for tag in self.currentImages[self.stackedWidget.currentIndex()].tags:
                tags += tag + ", "
            tags = tags[:-2]
            self.tagsEdit.setText(tags)
        else:
            self.setWindowTitle(self.WINDOW_TITLE)
            self.tagsEdit.setText("")

    def _prevImage(self):
        index = self.stackedWidget.currentIndex() - 1
        if index < 0:
            index = self.stackedWidget.count() - 1
        self._selectImage(index)

    def _nextImage(self):
        index = self.stackedWidget.currentIndex() + 1
        if index >= self.stackedWidget.count():
            index = 0
        self._selectImage(index)

    def _displayImages(self):
        # TODO optimize : do not delete everything everytime
        for i in reversed(range(self.stackedWidget.count())): 
            self.stackedWidget.widget(i).deleteLater()
        for image in self.currentImages:
            label = QtGui.QLabel()
            pixmap = QtGui.QPixmap(image.location)
            label.setPixmap(pixmap)
            self.stackedWidget.addWidget(label)
        self._selectImage(0)

    def _queryCollection(self):
        if self.collection:
            query = str(self.queryEdit.text())
            print query
            if query == "":
                self.currentImages = self.collection.images.values()
            else:
                self.currentImages = list(self.collection.query(query))
            self._displayImages()

    def _openCollection(self):
        dir = QtGui.QFileDialog.getExistingDirectory()
        if dir != "":
            self.collection = Collection(dir)
            self._queryCollection()

    def _scanCollection(self):
        if self.collection:
            self.collection.scan()
            self._queryCollection()

    def _saveCollection(self):
        if self.collection:
            self.collection.save()

    def _changeTags(self):
        # TODO add tags using a dialog
        pass

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    config = Config()
    window = TagGuiWindow(config)
    window.show()
    app.exec_()