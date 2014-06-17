import json

class Config:
	def __init__(self, filename = "config.json"):
		try:
			with open(filename, "r") as f:
				gayson = json.load(f)
				self.default_dir = gayson["default_dir"]
		except:
			pass