from pygame.surface import Surface
from sprite_manager import SpriteManager
from ui.button import Button
from ui.clickable import Clickable
from ui.specialist_panel import SpecialistPanel

__author__ = 'TriD'


class ClickableSpList(Clickable):
    def __init__(self, data, x, y):
        self.data = data
        self.surface = Surface((200, 170))
        self.x = x
        self.y = y
        self.up_button = Button(86, 0, 28, 21, callback=self.decrease_offset, sprite=SpriteManager().sprites['up_button'])
        self.down_button = Button(86, 142, 28, 21, callback=self.increase_offset, sprite=SpriteManager().sprites['down_button'])
        self.offset = 0
        self.items = [self.up_button, self.down_button]
        self.clickables = [self.up_button, self.down_button]
        self.reset()

    def update_specialists(self):
        self.shown_sp_panels = self.sp_panels[self.offset:self.offset + 2]
        for i in range(len(self.shown_sp_panels)):
            self.shown_sp_panels[i].y = i * 60 + 21

    def increase_offset(self):
        if self.offset < len(self.data.specialists) - 2:
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
        for item in self.shown_sp_panels:
            item.draw(self.surface)
        screen.blit(self.surface, (self.x, self.y))

    def is_pressed(self, wx, wy, button):
        x = wx - self.x
        y = wy - self.y
        for item in self.clickables:
            item.is_pressed(x, y)
        for item in self.shown_sp_panels:
            if item.is_pressed(x, y):
                if item.selected:
                    self.chosen.add(item.specialist)
                else:
                    self.chosen.remove(item.specialist)

    def reset(self):
        free_specialists = [sp for sp in self.data.specialists if not sp.occupied]
        self.sp_panels = [SpecialistPanel(0, 0, specialist, True) for specialist in free_specialists]
        self.update_specialists()
        self.chosen = set()