import os
import json
import hashlib
import re
from Image import *

def hashfile(afile, blocksize=65536):
    with open(afile, "rb") as f:
        hasher = hashlib.sha1()
        buf = f.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(blocksize)
        return str(hasher.hexdigest())

class Collection:
    TAGFILE = ".tagger"
    def __init__(self, directory):
        if (directory[-1] != "/"):
            directory += "/"
        self.directory = directory
        self.subcollections = dict()
        self.load()

    # TODO optimize load and scan
    def load(self, filename=TAGFILE):
        self._load()
        self._createsubcollections()

    def save(self, filename=TAGFILE):
        self._save()
        for subcollection in self.subcollections.values():
            subcollection.save()

    def scan(self):
        self._scan()
        self._createsubcollections()
        for subcollection in self.subcollections.values():
            subcollection.scan()

    def __getitem__(self, name):
        hach = hashfile(name)
        return self.images[hach]

    def __setitem__(self, name, val):
        hach = hashfile(name)
        self.images[hach] = val

    def all_images(self):
        res = dict()
        res.update(self.images)
        for subcollection in self.subcollections.values():
            res.update(subcollection.all_images())
        return res

    def delete_image(self, image):
        os.remove(image.location)
        hach = hashfile(image.location)
        self._remove_image(hach)

    def _createsubcollections(self):
        for afile in os.listdir(self.directory):
            filename = self.directory + afile
            if (os.path.isdir(filename) and not filename in self.subcollections.keys()):
                self.subcollections[filename] = Collection(filename)

    def _load(self):
        self.images = {}
        try:
            with open(self.directory + self.TAGFILE, "r") as f:
                print("opening " + self.directory)
                data = json.load(f)
                for imagehash, img in data.items():
                    try:
                        image = Image(img['location'], img['tags'])
                        self.images[imagehash] = image
                    except NotImageError:
                        print(img['location'], " is not an image.")
        except IOError:
            print("could not open " + self.directory, ". No " + self.TAGFILE)
            self._scan()

    def _save(self):
        if len(self.images) > 0:
            print("saving " + str(len(self.images)) + " to " + self.directory + self.TAGFILE)
            with open(self.directory + self.TAGFILE, "w") as f:
                json.dump({imagehash: img.__dict__ for imagehash, img in self.images.items()}, f)

    def _scan(self):
        print("scanning " + self.directory)
        for afile in os.listdir(self.directory):
            filename = self.directory + afile
            try:
                img = Image(filename)
                self._add_image(filename)
            except NotImageError:
                print(filename, " is not an image")

    def _add_image(self, image, tags=[]):
        print(os.path.dirname(image), self.directory)
        if os.path.dirname(image) == self.directory[:-1]:
            hach = hashfile(image)
            if (hach not in self.images):
                self.images[hach] = Image(image, tags)
        else:
            for subcollection in self.subcollections.values():
                subcollection._add_image(image)

    def _remove_image(self, hach):
        if hach in self.images:
            del self.images[hach]
        else:
            for subcollection in self.subcollections.values():
                subcollection._remove_image(hach)

    # TODO query system : parenthesis and approximation
    def query(self, query):
        args = self._parseQueryArgs(query, "or")
        ret = set()
        for arg in args:
            if (" or " not in arg):
                ret = ret | set(self._queryAnd(arg))
            else:
                ret = self.query(arg)
        for subcollection in self.subcollections.values():
            t = subcollection.query(query)
            ret |= t
        return ret

    def _parseQueryArgs(self, query, operator):
        args = query.split(" " + operator + " ")
        for i in range(len(args)):
            args[i] = re.sub(r"[^a-zA-Z0-9 ]", "", args[i])
        return args

    def _queryAnd(self, query):
        args = self._parseQueryArgs(query, "and")
        res = set()
        for imagehash, img in self.images.items():
            tmp = True
            for arg in args:
                if (arg[:4] == "not " and arg[4:] not in img.tags):
                    pass
                elif (arg not in img.tags):
                    tmp = False
            if (tmp):
                res.add(img)
        return res

    def _queryOr(self, query):
        args = self._parseQueryArgs(query, "or")
        res = set()
        for imagehash, img in self.images.items():
            tmp = False
            for arg in args:
                if (arg[:4] == "not " and arg[4:] in img.tags):
                    pass
                elif (arg in img.tags):
                    tmp = True
            if (tmp):
                res.add(img)
        return res