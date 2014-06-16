

class Image:
	def __init__(self, location, tags, hash = None):
		self.tags = tags
		self.location = location
		self.hash = hash

	def __repr__(self):
		return str(self.__dict__)

	def addTag(self, tag):
		if tag not in self.tags:
			self.tags.append(tag)

	def removeTag(self, tag):
		self.tags.remove(tag)

if __name__ == '__main__':
	img = Image("05.jpg", ["caca", "brol"])
	assert(str(img) == "{'hash': None, 'location': '05.jpg', 'tags': ['caca', 'brol']}")
	img.addTag("caca")
	assert(str(img) == "{'hash': None, 'location': '05.jpg', 'tags': ['caca', 'brol']}")
	img.addTag("truc")
	assert(str(img) == "{'hash': None, 'location': '05.jpg', 'tags': ['caca', 'brol', 'truc']}")
	img.removeTag("caca")
	assert(str(img) == "{'hash': None, 'location': '05.jpg', 'tags': ['brol', 'truc']}")