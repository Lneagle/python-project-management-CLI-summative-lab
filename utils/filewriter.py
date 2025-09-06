import json

def filewriter(path, collection):
    with open(path, "w") as file:
        data = []
        for item in collection:
            data.append(item.serialize())
        json.dump(data, file)