from PyQt4 import QtGui, QtCore
import sys
from copy import deepcopy

from Config import Config
from Collection import Collection
import MainWindowUI

class TagGuiWindow(QtGui.QMainWindow, MainWindowUI.Ui_MainWindow):
    WINDOW_TITLE = "TagGui"
    def __init__(self, config, parent=None):
        super(TagGuiWindow, self).__init__(parent)
        self.setupUi(self)
        self.setMouseTracking(True)
        self.centralwidget.setMouseTracking(True)
        self.imageLabel.setMouseTracking(True)
        self.actionOpen.triggered.connect(self._openCollection)
        self.actionScan.triggered.connect(self._scanCollection)
        self.actionSave.triggered.connect(self._saveCollection)
        self.actionExit.triggered.connect(self.close)

        self.queryEdit.returnPressed.connect(self._queryCollection)
        self.tagsEdit.returnPressed.connect(self._changeTags)

        self.collection = None
        self.currentImages = []
        self.currentIndex = 0
        self.oldMousePosition = [0, 0]
        self.qImages = {}

    def keyPressEvent(self, event):
        """ """
        if event.key() == QtCore.Qt.Key_Left:
            self._prevImage()
        elif event.key() == QtCore.Qt.Key_Right:
            self._nextImage()
        elif event.key() == QtCore.Qt.Key_Escape:
            self.setFocus()
        elif event.key() == QtCore.Qt.Key_Space:
            self.currentImagePosition = [0, 0]
            self._showImage()

    def mouseMoveEvent(self, event):
        deltaX, deltaY = event.x() - self.oldMousePosition[0], event.y() - self.oldMousePosition[1]
        self.oldMousePosition = [event.x(), event.y()]
        if event.buttons() & QtCore.Qt.LeftButton:
            self.currentImagePosition[0] -= deltaX
            self.currentImagePosition[1] -= deltaY
            self._updateImage()

    def wheelEvent(self, event):
        """ docstring """
        image = self._getCurrentImage()
        if image:
            step = event.delta() / 5.0
            pixmap = self.imageLabel.pixmap()
            w, h = pixmap.width(), pixmap.height()
            self.currentImageZoom = [w + step, h + step]
            self._updateImage()

    def resizeEvent(self, event):
        self.size = event.size()
        self.deltaSize = event.size()-event.oldSize()
        self.centralwidget.resize(self.centralwidget.size() + (self.deltaSize))

    def _getCurrentImage(self):
        if 0 <= self.currentIndex < len(self.currentImages):
            return self.currentImages[self.currentIndex]
        else:
            return None

    def _loadImage(self, image):
        if image.location not in self.qImages:
            # TODO magic number here
            while (len(self.qImages) > 500):
                self.qImages.pop(self.qImages.keys()[0])
            self.qImages[image.location] = QtGui.QImage(image.location)

    def _showImage(self):
        image = self._getCurrentImage()
        window_title = self.WINDOW_TITLE
        tags = ""
        if image:
            # window title
            window_title += " - " + image.location
            # tags
            for tag in image.tags:
                tags += tag + ", "
            tags = tags[:-2]
            # image
            self._loadImage(image)
            x, y = self.qImages[image.location].width(), self.qImages[image.location].height()
            self.currentImagePosition = [0, 0]
            self.currentImageRect = [x, y]
            self.currentImageZoom = deepcopy(self.currentImageRect)
            self._updateImage()
        self.setWindowTitle(window_title)
        self.tagsEdit.setText(tags)

    def _updateImage(self):
        image = self._getCurrentImage()
        pixmap = QtGui.QPixmap()
        if image:
            x, y = self.qImages[image.location].width(), self.qImages[image.location].height()
            pixmap = QtGui.QPixmap.fromImage(
                self.qImages[image.location]
                    .copy(
                        self.currentImagePosition[0], 
                        self.currentImagePosition[1],
                        self.currentImageRect[0], 
                        self.currentImageRect[1])
                    .scaled(
                        self.currentImageZoom[0], 
                        self.currentImageZoom[1], 
                        QtCore.Qt.KeepAspectRatio, 
                        QtCore.Qt.SmoothTransformation))
            # TODO enlarge pixmap
        self.imageLabel.setPixmap(pixmap)

    def _prevImage(self):
        self.currentIndex -= 1
        if self.currentIndex < 0:
            self.currentIndex = len(self.currentImages) - 1
        self._showImage()

    def _nextImage(self):
        self.currentIndex += 1
        if self.currentIndex >= len(self.currentImages):
            self.currentIndex = 0
        self._showImage()

    def _showCollection(self):
        if self.currentIndex < 0:
            self.currentIndex = 0
        elif self.currentIndex >= len(self.currentImages):
            self.currentIndex = len(self.currentImages) - 1
        self._showImage()

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
            self._queryCollection()

    def _scanCollection(self):
        """ Scan current collection for changes. Then load new images and show them """
        if self.collection:
            self.collection.scan()
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