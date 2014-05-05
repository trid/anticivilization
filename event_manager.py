__author__ = 'TriD'


class EventManager:
    def __init__(self):
        self.listeners = {}
        self.stack = []

    def purge(self):
        self.listeners.clear()
        self.stack = []

    def dispatch(self, type, message):
        self.listeners[type](message)

    def push(self, message):
        self.stack.append(message)