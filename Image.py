import os

class Image:
	def __init__(self, location = None, tags = [], json = None):
		if (json):
			self.tags = json["tags"]
			self.location = json["location"]
		else:
			self.tags = tags
			self.location = location

	def __repr__(self):
		return str(self.__dict__)

	def isImage(self):
		return os.path.isfile(self.location) and self.location.split(".")[-1].lower() in ["jpg", "jpeg", "png"]

	def addTags(self, tags):
		for tag in tags:
			self.addTag(tag)

	def addTag(self, tag):
		if tag not in self.tags:
			self.tags.append(tag)

	def removeTags(self, tags):
		for tag in tags:
			self.removeTag(tag)

	def removeTag(self, tag):
		if tag in self.tags:
			self.tags.remove(tag)

if __name__ == '__main__':
	img = Image("05.jpg", ["caca", "brol"])
	assert(str(img) == "{'location': '05.jpg', 'tags': ['caca', 'brol']}")
	img.addTag("caca")
	assert(str(img) == "{'location': '05.jpg', 'tags': ['caca', 'brol']}")
	img.addTag("truc")
	assert(str(img) == "{'location': '05.jpg', 'tags': ['caca', 'brol', 'truc']}")
	img.removeTag("caca")
	assert(str(img) == "{'location': '05.jpg', 'tags': ['brol', 'truc']}")