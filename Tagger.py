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

	def query2(self, query):
		args = self.parseQueryArgs(query, "or")
		print(args)
		ret = set()
		for arg in args:
			if (" or " not in arg):
				ret = ret | set(self.queryAnd(arg))
			# elif (" and " not in arg):
			# 	ret = ret & self.queryOr(arg)
			else:
				ret = self.query2(arg)
		return ret

		

	def parseQueryArgs(self, query, operator):
		args = query.split(" " + operator + " ")
		for i in range(len(args)):
			args[i] = re.sub(r"[^a-zA-Z0-9 ]", "", args[i])
		return args

	def queryAnd(self, query):
		args = self.parseQueryArgs(query, "and")
		print(args)
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
	# query = tagger.query("01 and Dragon Ball or not Dragon Ball or not 03")
	# query = tagger.query("a\"): print(\"caca\"); a=\"\" \nif(\"")
	# print(query)
	# queryAnd = tagger.queryAnd("01 and Dragon Ball and Dragon Ball")
	# print(queryAnd)
	# queryOr = tagger.queryOr("01 or 03")
	# print(queryOr)
	# query2 = tagger.query2("01 and Dragon Ball or 03 and Dragon Ball")
	# print(query2)
	# negquery = tagger.query2("01 and not Dragon Bal and not caca and not Dragon Ball or Dragon Ball")
	# print(negquery)
	negquery2 = tagger.query2("01 and Dragon Ball or not 03 and Dragon Ball")
	print(negquery2)