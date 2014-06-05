import pygame
import application

__author__ = 'TriD'


MESSAGE_MOUSE_UP = 'MOUSE_UP'
MESSAGE_QUIT = 'quit'


class EventManager:
    def __init__(self):
        self.listeners = {}
        self.stack = []

    def purge(self):
        self.listeners.clear()
        self.stack = []

    def dispatch(self, message_type, message):
        self.listeners[message_type](message)

    def push(self, message):
        self.stack.append(message)

    def add_listener(self, message_type, listener):
        if message_type not in self.listeners:
            self.listeners[message_type] = []
        self.listeners[message_type].append(listener)

    def process(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT and MESSAGE_QUIT not in self.listeners:
                application.application.running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                for listener in self.listeners.get(MESSAGE_MOUSE_UP, ()):
                    listener.on_click(event.pos[0], event.pos[1], event.button)


event_manager = EventManager()