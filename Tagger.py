from Collection import Collection
from UI import *
from Config import Config
import argparse

parser = argparse.ArgumentParser(description="Tag your pictures and view it with your favorite image viewer !")
parser.add_argument("-D", "--directory", type=str, help="The pictures directory")
parser.add_argument("-G", "--gui", action="store_true", help="Switch on Gtk+ interface. Ignores every other command line arguments and uses the config file")
parser.add_argument("-S", "--scan", action="store_true", help="Scan directory for new files and removed files")
args = parser.parse_args()

config = Config()

if (args.gui):
	window = MainWindow(config)
else:
	if (args.directory):
		directory = args.directory
	else:
		directory = config.default_dir
	collection = Collection(directory)
	collection.load(args.scan)
	collection.save()