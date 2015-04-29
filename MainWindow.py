# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt.ui'
#
# Created: Thu Apr 30 00:09:41 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 50, 641, 491))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.queryEdit = QtGui.QLineEdit(self.centralwidget)
        self.queryEdit.setGeometry(QtCore.QRect(20, 10, 641, 22))
        self.queryEdit.setObjectName(_fromUtf8("queryEdit"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuImage = QtGui.QMenu(self.menubar)
        self.menuImage.setObjectName(_fromUtf8("menuImage"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuCollection = QtGui.QMenu(self.menubar)
        self.menuCollection.setObjectName(_fromUtf8("menuCollection"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew = QtGui.QAction(MainWindow)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionScan = QtGui.QAction(MainWindow)
        self.actionScan.setObjectName(_fromUtf8("actionScan"))
        self.actionAdd_tags = QtGui.QAction(MainWindow)
        self.actionAdd_tags.setObjectName(_fromUtf8("actionAdd_tags"))
        self.actionRemove_tags = QtGui.QAction(MainWindow)
        self.actionRemove_tags.setObjectName(_fromUtf8("actionRemove_tags"))
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionExit)
        self.menuImage.addAction(self.actionAdd_tags)
        self.menuImage.addAction(self.actionRemove_tags)
        self.menuCollection.addAction(self.actionScan)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuCollection.menuAction())
        self.menubar.addAction(self.menuImage.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuImage.setTitle(_translate("MainWindow", "Image", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
        self.menuCollection.setTitle(_translate("MainWindow", "Collection", None))
        self.actionNew.setText(_translate("MainWindow", "New", None))
        self.actionOpen.setText(_translate("MainWindow", "Open", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))
        self.actionScan.setText(_translate("MainWindow", "Scan", None))
        self.actionAdd_tags.setText(_translate("MainWindow", "Add tags", None))
        self.actionRemove_tags.setText(_translate("MainWindow", "Remove tags", None))

