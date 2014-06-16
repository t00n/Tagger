import os

class Image:
	def __init__(self, hach = None, location = None, tags = [], json = None):
		if (json):
			self.tags = json["tags"]
			self.location = json["location"]
			self.hash = json["hash"]
		else:
			self.tags = tags
			self.location = location
			self.hash = hach

	def __repr__(self):
		return str(self.__dict__)

	# TODO Image.isImage
	@staticmethod
	def isImage(filename):
		return os.path.isfile(filename) and filename.split(".")[-1] in ["jpg", "jpeg", "png"]

	def addTag(self, tag):
		if tag not in self.tags:
			self.tags.append(tag)

	def removeTag(self, tag):
		self.tags.remove(tag)

if __name__ == '__main__':
	img = Image("caca", "05.jpg", ["caca", "brol"])
	assert(str(img) == "{'hash': 'caca', 'location': '05.jpg', 'tags': ['caca', 'brol']}")
	img.addTag("caca")
	assert(str(img) == "{'hash': 'caca', 'location': '05.jpg', 'tags': ['caca', 'brol']}")
	img.addTag("truc")
	assert(str(img) == "{'hash': 'caca', 'location': '05.jpg', 'tags': ['caca', 'brol', 'truc']}")
	img.removeTag("caca")
	assert(str(img) == "{'hash': 'caca', 'location': '05.jpg', 'tags': ['brol', 'truc']}")