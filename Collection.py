import os
import json
import hashlib
import re
from Image import Image

def hashfile(afile, blocksize=65536):
    hasher = hashlib.sha512()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    return str(hasher.hexdigest())

class Collection:
	TAGFILE = ".tagger"
	def __init__(self, directory):
		if (directory[-1] != "/"):
			directory = directory + "/"
		self.directory = directory
		os.chdir(self.directory)

	def load(self, scan = True):
		self.images = {}
		try:
			with open(self.TAGFILE, "r") as f:
				gayson = json.load(f)
				for imagehash, img in gayson.iteritems():
					image = Image(json=img)
					if (image.isImage()):
						self.images[imagehash] = image
		except:
			self.scan()
		if (scan):
			self.scan()

	def save(self):
		with open(self.TAGFILE, "w") as f:
			json.dump(dict((imagehash, img.__dict__) for imagehash, img in self.images.iteritems()), f)

	def scan(self, directory = "."):
		for afile in os.listdir(directory):
			filename = directory + "/" + afile
			img = Image(filename)
			if (img.isImage()):
				self.addImage(filename)
			elif (os.path.isdir(filename)):
				self.scan(filename)

	def addImage(self, afile):
		with open(afile) as f:
			hach = hashfile(f)
			if (hach not in self.images):
				self.images[hach] = Image(afile)

	def query(self, query):
		args = self.parseQueryArgs(query, "or")
		ret = set()
		for arg in args:
			if (" or " not in arg):
				ret = ret | set(self.queryAnd(arg))
			else:
				ret = self.query(arg)
		return ret

	def parseQueryArgs(self, query, operator):
		args = query.split(" " + operator + " ")
		for i in range(len(args)):
			args[i] = re.sub(r"[^a-zA-Z0-9 ]", "", args[i])
		return args

	def queryAnd(self, query):
		args = self.parseQueryArgs(query, "and")
		res = set()
		for imagehash, img in self.images.iteritems():
			tmp = True
			for arg in args:
				if (arg[:4] == "not " and arg[4:] not in img.tags):
					pass
				elif (arg not in img.tags):
					tmp = False
			if (tmp):
				res.add(img)
		return res

	def queryOr(self, query):
		args = self.parseQueryArgs(query, "or")
		res = set()
		for imagehash, img in self.images.iteritems():
			tmp = False
			for arg in args:
				if (arg[:4] == "not " and arg[4:] in img.tags):
					pass
				elif (arg in img.tags):
					tmp = True
			if (tmp):
				res.add(img)
		return res

if __name__ == '__main__':
	collection = Collection("test")
	collection.load()
	queryAnd = collection.queryAnd("01 and Dragon Ball")
	assert(str(queryAnd) == "set([{'location': u'./01.jpg', 'tags': [u'01', u'Dragon Ball']}])")
	queryOr = collection.queryOr("01 or 03")
	assert(str(queryOr) == "set([{'location': u'./03.jpg', 'tags': [u'03', u'Dragon Ball']}, {'location': u'./01.jpg', 'tags': [u'01', u'Dragon Ball']}])")
	query = collection.query("01 and Dragon Ball or 03 and Dragon Ball")
	assert(str(query) == "set([{'location': u'./03.jpg', 'tags': [u'03', u'Dragon Ball']}, {'location': u'./01.jpg', 'tags': [u'01', u'Dragon Ball']}])")
	negquery = collection.query("01 and not Dragon Bal and not caca and not Dragon Ball or Dragon Ball")
	assert(str(negquery) == "set([{'location': u'./soustest/05.jpg', 'tags': [u'05', u'Dragon Ball']}, {'location': u'./03.jpg', 'tags': [u'03', u'Dragon Ball']}, {'location': u'./01.jpg', 'tags': [u'01', u'Dragon Ball']}, {'location': u'./soustest/06.jpg', 'tags': [u'06', u'Dragon Ball']}])")
	