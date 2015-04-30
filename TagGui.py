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
        self.tagsEdit.returnPressed.connect(self._changeTags)

        self.collection = None
        self.currentImages = []
        self.qImages = {}

    def keyPressEvent(self, event):
        """ """
        # TODO add move image (maybe with drag and drop ?)
        if event.key() == QtCore.Qt.Key_Left:
            self._prevImage()
        elif event.key() == QtCore.Qt.Key_Right:
            self._nextImage()
        elif event.key() == QtCore.Qt.Key_Escape:
            self.setFocus()

    def wheelEvent(self, event):
        """ docstring """
        image = self._getCurrentImage()
        if image:
            step = event.delta() / 30.0
            label = self.stackedWidget.currentWidget()
            pixmap = label.pixmap()
            w, h = pixmap.width(), pixmap.height()
            newW, newH = w + step, h + step
            pixmap = QtGui.QPixmap.fromImage(self.qImages[image.location].scaled(newW, newH,                           QtCore.Qt.KeepAspectRatio, 
                                            QtCore.Qt.FastTransformation))
            label.setPixmap(pixmap)

    def _getCurrentImage(self):
        if len(self.currentImages) > 0:
            return self.currentImages[self.stackedWidget.currentIndex()]
        else:
            return None

    def _showImage(self, index):
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
        self._showImage(index)

    def _nextImage(self):
        index = self.stackedWidget.currentIndex() + 1
        if index >= self.stackedWidget.count():
            index = 0
        self._showImage(index)

    def _showCollection(self):
        # TODO optimize : do not delete everything everytime
        for i in reversed(range(self.stackedWidget.count())): 
            self.stackedWidget.widget(i).deleteLater()
        for image in self.currentImages:
            if image.location in self.qImages:
                label = QtGui.QLabel()
                pixmap = QtGui.QPixmap.fromImage(self.qImages[image.location])
                label.setPixmap(pixmap)
                self.stackedWidget.addWidget(label)
            else:
                print "image ", image.location, " was not loaded. WTF"
        self._showImage(0)

    def _loadCollection(self):
        """ Load collection in a dict of QImage to prevent multiple loading """
        # TODO images are never deleted. Could be bad for memory obviously. Qt deletes ?
        if self.collection:
            for image in self.collection.images.itervalues():
                if image.location not in self.qImages:
                    self.qImages[image.location] = QtGui.QImage(image.location)

    # Qt Actions
    def _queryCollection(self):
        if self.collection:
            query = str(self.queryEdit.text()).strip()
            if query == "":
                self.currentImages = self.collection.images.values()
            else:
                self.currentImages = list(self.collection.query(query))
            self._showCollection()

    def _openCollection(self):
        dir = QtGui.QFileDialog.getExistingDirectory()
        if dir != "":
            self.collection = Collection(dir)
            self._loadCollection()
            self._queryCollection()

    def _scanCollection(self):
        """ Scan current collection for changes. Then load new images and show them """
        if self.collection:
            self.collection.scan()
            self._loadCollection()
            self._queryCollection()

    def _saveCollection(self):
        if self.collection:
            self.collection.save()

    def _changeTags(self):
        """ Retrieve tags from tags line edit and assign them to current image """
        image = self._getCurrentImage()
        if image:
            tags = map(lambda s: s.strip(), str(self.tagsEdit.text()).split(","))
            image.tags = tags

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    config = Config()
    window = TagGuiWindow(config)
    window.show()
    app.exec_()