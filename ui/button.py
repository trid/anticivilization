__author__ = 'TriD'


class Button:
    def __init__(self, x, y, w, h, name=None, caller=None, sprite=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.callback = None
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

        if self.callback:
            if self.caller:
                self.callback(self.caller)
            else:
                self.callback()

        return True

    def draw(self, screen):
        if self.sprite:
            screen.blit(self.sprite, (self.x, self.y))