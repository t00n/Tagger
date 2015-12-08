from Collection import Collection
from Config import Config

import argh

def scan(directory):
	collection = Collection(directory)
	collection.scan()
	collection.save()

def query(directory, query):
	collection = Collection(directory)
	print(collection.query(query))

@argh.arg('images', nargs='+')
@argh.arg('tags', nargs='+')
def add(images, tags):
	pass

@argh.arg('images', nargs='+')
@argh.arg('tags', nargs='+')
def remove(images, tags):
	print(images)
	print(tags)

parser = argh.ArghParser()
parser.add_commands([scan, query, add, remove])

if __name__ == '__main__':
    parser.dispatch()
