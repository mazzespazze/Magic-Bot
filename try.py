import json

class JsonSerializable(object):
    def toJson(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return self.toJson()


class FileItem(JsonSerializable):
    def __init__(self, fname):
        self.fname = fname
