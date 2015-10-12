import json

with open(".tagger") as f:
    gayson = json.load(f)

newtagger = {}

for hach, image in gayson.iteritems():
    location = image["location"].split("/")
    print location
    if len(location) > 2:
        path = "/".join(location[:-1])
        try:
            with open(path + "/.tagger", "r") as f:
                subgayson = json.load(f)
        except:
            subgayson = {}
        subgayson[hach] = image
        with open(path + "/.tagger", "w") as f:
            json.dump(subgayson, f)
    else:
        newtagger[hach] = image

with open(".tagger", "w") as f:
    json.dump(newtagger, f)