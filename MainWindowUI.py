# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt.ui'
#
# Created: Thu Apr 30 17:10:10 2015
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
        self.queryEdit = QtGui.QLineEdit(self.centralwidget)
        self.queryEdit.setGeometry(QtCore.QRect(70, 10, 591, 22))
        self.queryEdit.setAutoFillBackground(True)
        self.queryEdit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.queryEdit.setObjectName(_fromUtf8("queryEdit"))
        self.tagsEdit = QtGui.QLineEdit(self.centralwidget)
        self.tagsEdit.setGeometry(QtCore.QRect(70, 40, 591, 22))
        self.tagsEdit.setAutoFillBackground(True)
        self.tagsEdit.setObjectName(_fromUtf8("tagsEdit"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 63, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 63, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.imageLabel = QtGui.QLabel(self.centralwidget)
        self.imageLabel.setGeometry(QtCore.QRect(10, 100, 651, 431))
        self.imageLabel.setText(_fromUtf8(""))
        self.imageLabel.setObjectName(_fromUtf8("imageLabel"))
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
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionScan)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionExit)
        self.menuImage.addAction(self.actionAdd_tags)
        self.menuImage.addAction(self.actionRemove_tags)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuImage.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "TagGui", None))
        self.label.setText(_translate("MainWindow", "Query :", None))
        self.label_2.setText(_translate("MainWindow", "Tags :", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuImage.setTitle(_translate("MainWindow", "Image", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
        self.actionNew.setText(_translate("MainWindow", "New", None))
        self.actionOpen.setText(_translate("MainWindow", "Open", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))
        self.actionScan.setText(_translate("MainWindow", "Scan", None))
        self.actionAdd_tags.setText(_translate("MainWindow", "Add tags", None))
        self.actionRemove_tags.setText(_translate("MainWindow", "Remove tags", None))
        self.actionSave.setText(_translate("MainWindow", "Save", None))

