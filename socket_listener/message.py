class Message(object):
    def __init__(self, identifier, payload):
        self.identifier = identifier
        self.payload = payload

    def __str__(self):
        return "{}::{}".format(self.identifier, self.payload)