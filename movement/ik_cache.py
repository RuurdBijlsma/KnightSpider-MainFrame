import json
import os


class IKCache(object):
    def __init__(self, file_location):
        self.file = None
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

    def open_write(self):
        self.file = open(self.file_location, 'w')

    def close(self):
        self.file.close()
        self.file = None

    def export(self):
        j = json.dumps(self.points)
        if self.file is None:
            self.open_write()

        self.file.write(j)
        return j

    def clear(self):
        os.remove(self.file_location)
        self.points = {}
