from event_manager import event_manager

__author__ = 'TriD'


class Application:
    def __init__(self):
        self.states = []
        self.running = True

    def push_state(self, state):
        self.states.append(state)

    def pop_state(self):
        if self.states:
            self.states.pop()

    def process(self):
        event_manager.process()
        self.states[-1].process()

application = Application()