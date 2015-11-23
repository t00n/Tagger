import os

class NotImageError(Exception):
	pass

class Image:
	EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".jpe"]
	def __init__(self, location = None, tags = []):
		self.setTags(tags)
		self.location = location
		if not self._isImage():
			raise NotImageError

	def __repr__(self):
		return str(self.__dict__)

	def _isImage(self):
		return os.path.isfile(self.location) and os.path.splitext(self.location)[1].lower() in self.EXTENSIONS

	def setTags(self, tags):
		self.tags = tags

	def getTags(self):
		return self.tags

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