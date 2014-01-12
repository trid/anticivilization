from ui.clickable import Clickable

__author__ = 'TriD'


class Button(Clickable):
    def __init__(self, x, y, w, h, name=None, caller=None, sprite=None, callback=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.callback = callback
        self.active = True
        self.name = name
        self.caller = caller
        self.sprite = sprite

    def is_pressed(self, x, y):
        if not self.active:
            return False
        if x < self.x:
            return False
        elif x > self.x + self.w:
            return False
        elif y < self.y:
            return False
        elif y > self.y + self.h:
            return False

        self.run_callback()

        return True

    def draw(self, screen):
        if self.sprite:
            screen.blit(self.sprite, (self.x, self.y))

    def run_callback(self):
        if self.callback:
            if self.caller:
                self.callback(self.caller)
            else:
                self.callback()