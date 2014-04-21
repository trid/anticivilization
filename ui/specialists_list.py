from pygame.surface import Surface
from sprite_manager import SpriteManager
from ui.button import Button
from ui.clickable import Clickable
from ui.specialist_panel import SpecialistPanel

__author__ = 'TriD'


class SpecialistsList(Clickable):
    def __init__(self, data, x, y):
        self.data = data
        self.surface = Surface((200, 420))
        self.x = x
        self.y = y
        self.up_button = Button(86, 0, 28, 21, callback=self.decrease_offset, sprite=SpriteManager().sprites['up_button'])
        self.down_button = Button(86, 381, 28, 21, callback=self.increase_offset, sprite=SpriteManager().sprites['down_button'])
        self.offset = 0
        self.items = [self.up_button, self.down_button]
        self.clickables = [self.up_button, self.down_button]
        self.update_specialists()

    def update_specialists(self):
        window = self.data.specialists[self.offset:self.offset + 6]
        self.items = [self.up_button, self.down_button]
        for i in range(len(window)):
            self.items.append(SpecialistPanel(0, i * 60 + 21, window[i]))

    def increase_offset(self):
        if self.offset < len(self.data.specialists) - 6:
            self.offset += 1
            self.update_specialists()

    def decrease_offset(self):
        if self.offset > 0:
            self.offset -= 1
            self.update_specialists()

    def draw(self, screen):
        self.surface.fill(0x000000)
        for item in self.items:
            item.draw(self.surface)
        screen.blit(self.surface, (self.x, self.y))

    def is_pressed(self, wx, wy, button):
        x = wx - self.x
        y = wy - self.y
        for item in self.clickables:
            item.is_pressed(x, y, button)