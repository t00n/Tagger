from Image import Image
from ConfigParser import ConfigParser
import os
import json

class Tagger:
	TAGFILE = ".tagger"
	def __init__(self, directory):
		self.directory = directory
		self.parseTags()

	def parseTags(self):
		self.images = {}
		# check if file exists else create it
		with open(self.directory + self.TAGFILE, "r") as f:
			gayson = json.load(f)
			for img, tags in gayson.iteritems():
				self.images[img] = Image(img, tags)
				# check if file still exists, if not search it (by hash for example)
			f.close()
		# list all image files recursively and add them to .tagger if not already in it

if __name__ == '__main__':
	folder = "test/"
	tagger = Tagger(folder)