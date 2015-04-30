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

        self.actionAdd_tags.triggered.connect(self._addTags)
        self.actionRemove_tags.triggered.connect(self._removeTags)

        
    def keyPressEvent(self, event):
        """ """
        if event.key() == QtCore.Qt.Key_Left:
            self._prevImage()
        elif event.key() == QtCore.Qt.Key_Right:
            self._nextImage()
        elif event.key() == QtCore.Qt.Key_Escape:
            self.setFocus()
        elif event.key() == QtCore.Qt.Key_Enter:
            # TODO query
            pass

    def mousePressEvent(self, event):
        # TODO zoom in/out
        pass

    # TODO select current image (for tags)
    def _selectImage(self, index):
        self.stackedWidget.setCurrentIndex(index)
        self.windowTitle = self.WINDOW_TITLE + " - "

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

    def _openCollection(self):
        dir = QtGui.QFileDialog.getExistingDirectory()
        if dir != "":
            self.collection = Collection(dir)
            for image in self.collection.images.itervalues():
                label = QtGui.QLabel()
                pixmap = QtGui.QPixmap(image.location)
                label.setPixmap(pixmap)
                # label.setText(image.location)
                self.stackedWidget.addWidget(label)

    def _scanCollection(self):
        if self.collection:
            self.collection.scan()

    def _saveCollection(self):
        if self.collection:
            self.collection.save()

    def _addTags(self):
        # TODO add tags using a dialog
        pass

    def _removeTags(self):
        # TODO remove tags using a dialog
        pass

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    config = Config()
    window = TagGuiWindow(config)
    window.show()
    app.exec_()