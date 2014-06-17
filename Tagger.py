from Collection import Collection
from UI import *
import argparse

parser = argparse.ArgumentParser(description="Tag your pictures and view it with your favorite image viewer !")
parser.add_argument("-D", "--directory", type=str, help="The pictures directory")
parser.add_argument("-G", "--gui", action="store_true", help="Switch on Gtk+ interface. Ignores every other command line arguments and uses the config file")
parser.add_argument("-S", "--scan", action="store_true", help="Scan directory for new files and removed files")
args = parser.parse_args()
if (args.gui):
	# regarder la config et eventuellement demander un dossier
	config = Config()
	collection = Collection(config.default_dir)
	window = MainWindow(collection)
else:
	# use command line
	if (args.directory):
		directory = args.directory
	else:
		directory = "."
	collection = Collection(directory)
	collection.load(args.scan)
	collection.save()