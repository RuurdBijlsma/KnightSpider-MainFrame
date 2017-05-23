from threading import Thread
from threading import Event


class Deferred(object):
    def __init__(self):
        self._event = Event()
        self._rejected = False
        self._result = None

    def resolve(self, value):
        self._rejected = False
        self._result = value
        self._event.set()

    def reject(self, reason):
        self._rejected = True
        self._result = reason
        self._event.set()

    def promise(self):
        promise = Promise(self)
        return promise


class Promise(object):
    def __init__(self, deferred):
        self._deferred = deferred

    def then(self, resolved=None, rejected=None):
        defer = Deferred()

        def task():
            try:
                self._deferred._event.wait()
                if self._deferred._rejected:
                    result = self._deferred._result
                    if rejected:
                        result = rejected(self._deferred._result)

                    defer.reject(result)
                else:
                    result = self._deferred._result

                    if resolved:
                        result = resolved(self._deferred._result)

                    defer.resolve(result)
            except Exception as ex:
                defer.reject(ex.message)

        Thread(target=task).start()

        return defer.promise()

    def wait(self):
        self._deferred._event.wait()

    @staticmethod
    def wait_all(*args):
        for promise in args:
            promise.wait()