__author__ = 'TriD'


class Application:
    def __init__(self):
        self.states = []

    def push_state(self, state):
        self.states.append(state)

    def pop_state(self):
        if self.states:
            self.states.pop()

    def process(self):
        self.states.process()

application = Application()