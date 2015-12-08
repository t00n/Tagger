
ui:
	pyuic4 qt.ui -o MainWindowUI.py

clean:
	rm -rf __pycache__/

.PHONY: clean
