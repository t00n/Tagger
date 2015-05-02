all: main

ui:
	pyuic4 qt.ui -o MainWindowUI.py

main:
	python2 TagGui.py