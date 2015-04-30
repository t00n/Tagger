from Collection import Collection
from Config import Config
import argparse

parser = argparse.ArgumentParser(description="Tag your pictures and view it with your favorite image viewer !")
parser.add_argument("command", type=str, help="Command to use. One of scan, query, add or remove")
parser.add_argument("-d", "--directory", type=str, help="Collection directory")
parser.add_argument("-i", "--images", type=str, metavar='N', nargs='*', help="Pictures to modify")
parser.add_argument("-t", "--tags", type=str, metavar='N', nargs='*', help="Tags to add or remove")
parser.add_argument("-q", "--query", type=str, help="Query to send")
args = parser.parse_args()

config = Config()

if (args.directory):
	directory = args.directory
elif (args.images):
	directory = "/".join(args.images[0].split("/")[:-1])
else:
	directory = config.default_dir
collection = Collection(directory)
collection.load()
if (args.command == "scan"):
	collection.scan()
elif (args.command == "query"):
	if (args.query):
		# TODO query and show
		print collection.query(args.query)
	else:
		print "Command \"query\" needs a query"
elif (args.command == "add"):
	if (args.images and args.tags):
		for image in args.images:
			collection.addTags(image, args.tags)
	else:
		print "Command \"add\" needs an image and tags"
elif (args.command == "remove"):
	if (args.images and args.tags):
		for image in args.images:
			collection.removeTags(image, args.tags)
	else:
		print "Command \"remove\" needs an image and tags"

collection.save()