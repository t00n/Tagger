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

@argh.arg('images', nargs='+')
@argh.arg('tags', nargs='+')
def add(images, tags):
	for dirname, files in _get_collections(images).items():
		collection = Collection(dirname)
		for filename in files:
			collection.addTags(filename, tags)

@argh.arg('images', nargs='+')
@argh.arg('tags', nargs='+')
def remove(images, tags):
	for dirname, files in _get_collections(images).items():
		collection = Collection(dirname)
		for filename in files:
			collection.removeTags(filename, tags)

parser = argh.ArghParser()
parser.add_commands([scan, query, add, remove])

if __name__ == '__main__':
    parser.dispatch()
