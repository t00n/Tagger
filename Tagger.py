import os
import json
import gtk
import hashlib
import argparse
import re
from Image import Image
from ConfigParser import ConfigParser

def hashfile(afile, blocksize=65536):
    hasher = hashlib.sha512()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    return str(hasher.hexdigest())

class Tagger:
	TAGFILE = ".tagger"
	def __init__(self, directory):
		self.directory = directory
		os.chdir(self.directory)
		self.load()

	def load(self):
		self.images = {}
		try:
			print("loading...")
			with open(self.TAGFILE, "r") as f:
				gayson = json.load(f)
				for imagehash, img in gayson.iteritems():
					if (Image.isImage(img["location"])):
						self.images[imagehash] = Image(json=img)
				f.close()
		except:
			print("scanning...")
			self.scan()
		self.save()

	def save(self):
		with open(self.TAGFILE, "w") as f:
			json.dump(dict((imagehash, img.__dict__) for imagehash, img in self.images.iteritems()), f)
			f.close()

	def scan(self, directory = "."):
		for afile in os.listdir(directory):
			filename = directory + "/" + afile
			print(filename)
			if (Image.isImage(filename)):
				self.addImage(filename)
			elif (os.path.isdir(filename)):
				self.scan(filename)

	def addImage(self, afile):
		with open(afile) as f:
			hach = hashfile(f)
			if (hach not in self.images):
				self.images[hach] = Image(afile)
			f.close()

	def query(self, query, subset = None):
		query = "\"" + query
		index = [(m.start(0), m.end(0)) for m in re.finditer(" and | or ", query)]
		previous = 0
		for (start, end) in index:
			j = start + previous
			k = end + previous
			if (query[k:k+3] == "not"):
				k += 4
			query = query[:k] + "\"" + query[k:]
			query = query[:j] + "\" in image.tags" + query[j:]
			previous += len("\" in image.tagss")
		query = query + "\" in image.tags"
		print(query)

		ret = []
		for imagehash, image in self.images.iteritems():
			exec("if (" + query + "): ret.append(image)")
		print(ret)

class MainWindow(gtk.Window):
	def __init__(self, tagger):
		self.tagger = tagger
		gtk.Window.__init__(self)
		# self.show_all()
		# gtk.main()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Tag your pictures and view it with your favorite image viewer !")
	parser.add_argument("directory", type=str, help="The pictures directory")
	args = parser.parse_args()
	tagger = Tagger(args.directory)
	# print(tagger.images)
	# window = MainWindow(tagger)
	# queryAnd = tagger.query("01 and Dragon Ball or not Dragon Ball or not 03")
	queryAnd = tagger.query("a\"): print(\"caca\"); a=\"\" \nif(\"")
	# 01 in ... and Dragon Ball in ... or not 05 in ... or 03 in ... and Dragon Ball in ...
	print(queryAnd)