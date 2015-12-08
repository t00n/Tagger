import os

class NotImageError(Exception):
	pass

class Image:
	EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".jpe"]
	def __init__(self, location = None, tags = []):
		self.set_tags(tags)
		self.location = location
		if not self._is_image():
			raise NotImageError

	def _is_image(self):
		return os.path.isfile(self.location) and os.path.splitext(self.location)[1].lower() in self.EXTENSIONS

	def set_tags(self, tags):
		self.tags = tags

	def get_tags(self):
		return self.tags

	def add_tags(self, tags):
		for tag in tags:
			self.add_tag(tag)

	def add_tag(self, tag):
		if tag not in self.tags:
			self.tags.append(tag)

	def remove_tags(self, tags):
		for tag in tags:
			self.remove_tag(tag)

	def remove_tag(self, tag):
		if tag in self.tags:
			self.tags.remove(tag)