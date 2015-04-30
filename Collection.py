import os
import json
import hashlib
import re
from Image import Image

def hashfile(afile, blocksize=65536):
	with open(afile, "r") as f:
	    hasher = hashlib.sha1()
	    buf = f.read(blocksize)
	    while len(buf) > 0:
	        hasher.update(buf)
	        buf = f.read(blocksize)
	    return str(hasher.hexdigest())

class Collection:
	TAGFILE = ".tagger"
	def __init__(self, directory):
		if (directory[-1] != "/"):
			directory = directory + "/"
		os.chdir(directory)
		self.load()

	# TODO optimize load and scan
	def load(self):
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

	def save(self):
		with open(self.TAGFILE, "w") as f:
			json.dump(dict((imagehash, img.__dict__) for imagehash, img in self.images.iteritems()), f)

	def scan(self, directory = "."):
		for afile in os.listdir(directory):
			filename = directory + "/" + afile
			img = Image(filename)
			if (img.isImage()):
				self._addImage(filename)
			elif (os.path.isdir(filename)):
				self.scan(filename)

	def query(self, query):
		args = self._parseQueryArgs(query, "or")
		ret = set()
		for arg in args:
			if (" or " not in arg):
				ret = ret | set(self._queryAnd(arg))
			else:
				ret = self.query(arg)
		return ret

	def addTags(self, image, tags):
		hach = hashfile(image)
		if hach in self.images:
			self.images[hach].addTags(tags)
			print self.images[hach].tags

	def removeTags(self, image, tags):
		hach = hashfile(image)
		if hach in self.image:
			self.image[hach].removeTags(tags)

	def _addImage(self, afile):
		hach = hashfile(afile)
		if (hach not in self.images):
			self.images[hach] = Image(afile)

	def _parseQueryArgs(self, query, operator):
		args = query.split(" " + operator + " ")
		for i in range(len(args)):
			args[i] = re.sub(r"[^a-zA-Z0-9 ]", "", args[i])
		return args

	def _queryAnd(self, query):
		args = self._parseQueryArgs(query, "and")
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

	def _queryOr(self, query):
		args = self._parseQueryArgs(query, "or")
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
	_queryAnd = collection._queryAnd("01 and Dragon Ball")
	assert(str(_queryAnd) == "set([{'location': u'./01.jpg', 'tags': [u'01', u'Dragon Ball']}])")
	_queryOr = collection._queryOr("01 or 03")
	assert(str(_queryOr) == "set([{'location': u'./03.jpg', 'tags': [u'03', u'Dragon Ball']}, {'location': u'./01.jpg', 'tags': [u'01', u'Dragon Ball']}])")
	query = collection.query("01 and Dragon Ball or 03 and Dragon Ball")
	assert(str(query) == "set([{'location': u'./03.jpg', 'tags': [u'03', u'Dragon Ball']}, {'location': u'./01.jpg', 'tags': [u'01', u'Dragon Ball']}])")
	negquery = collection.query("01 and not Dragon Bal and not caca and not Dragon Ball or Dragon Ball")
	assert(str(negquery) == "set([{'location': u'./soustest/05.jpg', 'tags': [u'05', u'Dragon Ball']}, {'location': u'./03.jpg', 'tags': [u'03', u'Dragon Ball']}, {'location': u'./01.jpg', 'tags': [u'01', u'Dragon Ball']}, {'location': u'./soustest/06.jpg', 'tags': [u'06', u'Dragon Ball']}])")
	