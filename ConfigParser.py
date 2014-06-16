import json

class ConfigParser:
	def __init__(self, filename = "config.json"):
		with open(filename, "r") as f:
			f.close()