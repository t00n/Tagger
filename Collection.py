import os
import json
import hashlib
import re
from Image import Image

def hashfile(afile, blocksize=65536):
    with open(afile, "r") as f:
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
    def load(self):
        self.images = {}
        try:
            with open(self.directory + self.TAGFILE, "r") as f:
                print "opening " + self.directory
                gayson = json.load(f)
                for imagehash, img in gayson.iteritems():
                    image = Image(json=img)
                    if (image.isImage()):
                        self.images[imagehash] = image
        except IOError:
            print "could not open " + self.directory, ". No " + self.TAGFILE
            self._scan()
        self._checksubdir()

    def save(self):
        print "saving " + str(len(self.images)) + " to " + self.directory + self.TAGFILE
        newimages = {}
        for key, img in self.images.iteritems():
            if img.location.split("/")[-2] == self.directory.split("/")[-2]:
                newimages[key] = img
        with open(self.directory + self.TAGFILE, "w") as f:
            json.dump(dict((imagehash, img.__dict__) for imagehash, img in newimages.iteritems()), f)
        for subcollection in self.subcollections.itervalues():
            subcollection.save()

    def _checksubdir(self):
        for afile in os.listdir(self.directory):
            filename = self.directory + afile
            if (os.path.isdir(filename) and not filename in self.subcollections.itervalues()):
                self.subcollections[filename] = Collection(filename)

    def _scan(self):
        print "scanning " + self.directory
        for afile in os.listdir(self.directory):
            filename = self.directory + afile
            img = Image(filename)
            if (img.isImage()):
                self._addImage(filename)

    def scan(self):
        self._scan()
        self._checksubdir()
        for subcollection in self.subcollections.itervalues():
            subcollection.scan()


    def allimages(self):
        res = dict()
        res.update(self.images)
        for subcollection in self.subcollections.itervalues():
            res.update(subcollection.allimages())
        return res

    # TODO query system : parenthesis and approximation
    def query(self, query):
        args = self._parseQueryArgs(query, "or")
        ret = set()
        for arg in args:
            if (" or " not in arg):
                ret = ret | set(self._queryAnd(arg))
            else:
                ret = self.query(arg)
        for subcollection in self.subcollections.itervalues():
            t = subcollection.query(query)
            ret |= t
        return ret

    def deleteImage(self, image):
        os.remove(image.location)
        hach = hashfile(image.location)
        self._deleteImage(hach)

    def _deleteImage(self, hach):
        if hach in self.images:
            del self.images[hach]
        else:
            for subcollection in self.subcollections:
                subcollection._deleteImage(hach)

    def _addImage(self, afile):
        hach = hashfile(afile)
        if (hach not in self.images):
            self.images[hach] = Image(afile)

    def _parseQueryArgs(self, query, operator):
        args = query.split(" " + operator + " ")
        for i in range(len(args)):
            args[i] = re.sub(r"[^a-zA-Z0-9 ]", "", args[i])
        return args

    def _queryAnd(self, query):
        args = self._parseQueryArgs(query, "and")
        res = set()
        for imagehash, img in self.images.iteritems():
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
        for imagehash, img in self.images.iteritems():
            tmp = False
            for arg in args:
                if (arg[:4] == "not " and arg[4:] in img.tags):
                    pass
                elif (arg in img.tags):
                    tmp = True
            if (tmp):
                res.add(img)
        return res

if __name__ == '__main__':
    collection = Collection("test")
    collection.load()
    _queryAnd = collection._queryAnd("01 and Dragon Ball")
    assert(str(_queryAnd) == "set([{'location': u'./01.jpg', 'tags': [u'01', u'Dragon Ball']}])")
    _queryOr = collection._queryOr("01 or 03")
    assert(str(_queryOr) == "set([{'location': u'./03.jpg', 'tags': [u'03', u'Dragon Ball']}, {'location': u'./01.jpg', 'tags': [u'01', u'Dragon Ball']}])")
    query = collection.query("01 and Dragon Ball or 03 and Dragon Ball")
    assert(str(query) == "set([{'location': u'./03.jpg', 'tags': [u'03', u'Dragon Ball']}, {'location': u'./01.jpg', 'tags': [u'01', u'Dragon Ball']}])")
    negquery = collection.query("01 and not Dragon Bal and not caca and not Dragon Ball or Dragon Ball")
    assert(str(negquery) == "set([{'location': u'./soustest/05.jpg', 'tags': [u'05', u'Dragon Ball']}, {'location': u'./03.jpg', 'tags': [u'03', u'Dragon Ball']}, {'location': u'./01.jpg', 'tags': [u'01', u'Dragon Ball']}, {'location': u'./soustest/06.jpg', 'tags': [u'06', u'Dragon Ball']}])")
    