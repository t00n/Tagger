from PyQt4 import QtGui, QtCore
import sys

from Config import Config
import MainWindowUI

class TagGuiWindow(QtGui.QMainWindow, MainWindowUI.Ui_MainWindow):
    def __init__(self, config, parent=None):
        super(TagGuiWindow, self).__init__(parent)
        self.setupUi(self)

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	config = Config()
	window = TagGuiWindow(config)
	window.show()
	app.exec_()