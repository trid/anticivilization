import pygame
import application

__author__ = 'TriD'

MESSAGE_KEY_DOWN = 'KEY_DOWN'
MESSAGE_KEY_UP = 'KEY_UP'
MESSAGE_MOUSE_DOWN = 'MOUSE_DOWN'
MESSAGE_MOUSE_MOTION = 'MOUSE_MOTION'
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

    def remove_listener(self, message_type, listener):
        if message_type in self.listeners:
            listeners_list = self.listeners[message_type]
            if listener in listeners_list:
                listeners_list.remove(listener)

    def process(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT and MESSAGE_QUIT not in self.listeners:
                application.application.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for listener in self.listeners.get(MESSAGE_MOUSE_DOWN, ()):
                    if callable(listener):
                        listener(event.pos[0], event.pos[1], event.button)
                    else:
                        listener.process_message(event.pos[0], event.pos[1], event.button)
            elif event.type == pygame.MOUSEMOTION:
                for listener in self.listeners.get(MESSAGE_MOUSE_MOTION, ()):
                    if callable(listener):
                        listener(event.pos[0], event.pos[1])
                    else:
                        listener.process_message(event.pos[0], event.pos[1])
            elif event.type == pygame.MOUSEBUTTONUP:
                for listener in self.listeners.get(MESSAGE_MOUSE_UP, ()):
                    if callable(listener):
                        listener(event.pos[0], event.pos[1], event.button)
                    else:
                        listener.process_message(event.pos[0], event.pos[1], event.button)
            elif event.type == pygame.KEYUP:
                for listener in self.listeners.get(MESSAGE_KEY_UP, ()):
                    if callable(listener):
                        listener(event.key)
                    else:
                        listener.process_message(event.key)
            elif event.type == pygame.KEYDOWN:
                for listener in self.listeners.get(MESSAGE_KEY_DOWN, ()):
                    if callable(listener):
                        listener(event.key)
                    else:
                        listener.process_message(event.key)


event_manager = EventManager()