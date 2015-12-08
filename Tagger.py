from Collection import Collection
from Config import Config

import argh
import os
from collections import defaultdict

def scan(directory):
	collection = Collection(directory)
	collection.scan()
	collection.save()

def query(directory, query):
	collection = Collection(directory)
	print(collection.query(query))

def _get_collections(images):
	ret = defaultdict(lambda: [])
	for image in images:
		dirname = os.path.dirname(image)
		ret[dirname].append(image)
	return ret

@argh.arg('--images', nargs='+',type=str)
@argh.arg('--tags', nargs='+',type=str)
def add(images=[], tags=[]):
	for dirname, files in _get_collections(images).items():
		collection = Collection(dirname)
		for filename in files:
			collection[filename].add_tags(tags)
		collection.save('.tagger2')

@argh.arg('--images', nargs='+', type=str)
@argh.arg('--tags', nargs='+', type=str)
def remove(images=[], tags=[]):
	for dirname, files in _get_collections(images).items():
		collection = Collection(dirname)
		for filename in files:
			collection[filename].remove_tags(tags)
		collection.save('.tagger2')

@argh.arg('tags', nargs='+', type=str)
def addall(directory, tags):
	collection = Collection(directory)
	collection.add_all(tags)
	collection.save()

@argh.arg('tags', nargs='+', type=str)
def removeall(directory, tags):
	collection = Collection(directory)
	collection.remove_all(tags)
	collection.save()

parser = argh.ArghParser()
parser.add_commands([scan, query, add, remove, addall, removeall])

if __name__ == '__main__':
    parser.dispatch()
