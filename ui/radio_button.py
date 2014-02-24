from pygame.rect import Rect
from button import Button

__author__ = 'TriD'


class RadioButton(Button):
    def __init__(self, x, y, w, h):
        Button.__init__(self, x, y, w, h)
        self.checked = False

    def draw(self, screen):
        if self.checked:
            screen.blit(self.sprite, (self.x, self.y), Rect(0, 0, self.sprite.width, self.sprite.height/2))
        else:
            screen.blit(self.sprite, (self.x, self.y), Rect(0, self.sprite.height/2, self.sprite.width, self.sprite.height/2))

    def is_pressed(self, x, y):
        result = Button.is_pressed(self, x, y)
        if (result):
            self.checked = not self.checked