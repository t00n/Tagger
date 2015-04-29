from Collection import Collection
from UI import *
from Config import Config
import argparse

parser = argparse.ArgumentParser(description="Tag your pictures and view it with your favorite image viewer !")
parser.add_argument("-G", "--gui", action="store_true", help="Switch on Gtk+ interface. Ignores every other command line arguments and uses the config file")
parser.add_argument("command", type=str, help="Command to use. One of scan, query, add or remove")
parser.add_argument("-d", "--directory", type=str, help="Collection directory")
parser.add_argument("-i", "--image", type=str, help="Picture to modify")
parser.add_argument("-t", "--tags", type=str, metavar='N', nargs='*', help="Tags to add or remove")
parser.add_argument("-q", "--query", type=str, help="Query to send")
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
	collection.load()
	if (args.command == "scan"):
		collection.scan()
	elif (args.command == "query"):
		# TODO query and show
		print collection.query(args.query)
	elif (args.command == "add"):
		if (args.image and args.tags):
			collection.addTags(args.image, args.tags)
		else:
			print "Command \"add\" needs an image and tags"
	elif (args.command == "remove"):
		if (args.image and args.tags):
			collection.removeTags(args.image, args.tags)
		else:
			print "Command \"remove\" needs an image and tags"

	collection.save()