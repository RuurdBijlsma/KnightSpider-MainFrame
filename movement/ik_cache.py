import json


class IKCache(object):
    def __init__(self, file_location):
        self.file_location = file_location
        self.cache = {}

    def from_file(self):
        pass

    def export(self):
        j = json.dumps(self.cache)
        f = open(self.file_location, 'w')
        f.write(j)
        f.close()
