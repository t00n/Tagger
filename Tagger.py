from Collection import Collection
from UI import *
import argparse

parser = argparse.ArgumentParser(description="Tag your pictures and view it with your favorite image viewer !")
parser.add_argument("directory", type=str, help="The pictures directory")
args = parser.parse_args()
collection = Collection(args.directory)
window = MainWindow(collection)