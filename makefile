
ui:
	pyuic4 qt.ui -o MainWindowUI.py

clean:
	rm *.pyc
	rm -rf __pycache__/

mrproper: clean
