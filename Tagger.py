import os
import json
import gtk
import hashlib
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

	def save(self):
		with open(self.TAGFILE, "w") as f:
			json.dump(dict((imagehash, img.__dict__) for imagehash, img in self.images.iteritems()), f)
			f.close()

	def scan(self):
		for afile in os.listdir("."):
			if (Image.isImage(afile)):
				self.addImage(afile)
			elif (os.path.isdir(afile)):
				self.scan(afile)
		self.save()

	def addImage(self, afile):
		with open(afile) as f:
			hach = hashfile(f)
			if (hach not in self.images):
				self.images[hach] = Image(afile)
			f.close()

class MainWindow(gtk.Window):
	def __init__(self, tagger):
		self.tagger = tagger
		gtk.Window.__init__(self)
		# self.show_all()
		# gtk.main()

if __name__ == '__main__':
	folder = "test/"
	tagger = Tagger(folder)
	print(tagger.images)
	# tagger.scan()
	# print(tagger.images)
	window = MainWindow(tagger)