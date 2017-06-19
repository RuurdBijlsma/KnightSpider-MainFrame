import json
import os


class IKCache(object):
    def __init__(self, file_location):
        self.file_location = file_location
        self.points = {}

    def from_file(self):
        try:
            file = open(self.file_location, 'r')
            text = file.read()
            j = json.loads(text)
            self.points = j
            return j
        except Exception as e:
            print(e)

    def export(self):
        j = json.dumps(self.points)
        file = open(self.file_location, 'w')
        file.write(j)
        file.close()
        return j

    def clear(self):
        print("CLEARED CACHE")
        os.remove(self.file_location);
        self.points = {}
