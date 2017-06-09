class Message(object):
    def __init__(self, identifier, payload):
        self.identifier = identifier
        self.payload = payload

    @staticmethod
    def from_string(data):
        split = data.split("::")
        if not len(split) == 2:
            return None
        try:
            identifier = int(split[0])
            return Message(identifier, split[1])
        except ValueError:
            return None

    def __str__(self):
        return "{}::{}".format(self.identifier, self.payload)
