from ui.button import Button
from ui.dialog import Dialog
from ui.filtered_specialist_list import FilteredSpList
from ui.label import Label
import specialist
from sprite_manager import SpriteManager

__author__ = 'TriD'


class HuntingExpeditionDialog(Dialog):
    def __init__(self, uis):
        super(HuntingExpeditionDialog, self).__init__(400, 200, 200, 300)
        self.pop = 0
        self.uis = uis
        self.sp_list = FilteredSpList(uis.data, 0, 0, [specialist.WARRIOR, specialist.CHIEFTAIN])
        self.add(self.sp_list)
        sm = SpriteManager()
        self.send_button = Button(0, 271, 44, 21, sprite=sm.sprites['send_expedition_ok'],
                                  callback=uis.hunting_expedition_send)
        self.cancel_button = Button(100, 271, 60, 21, sprite=sm.sprites['cancel_button'],
                                    callback=uis.dialog_cancel_button)
        self.add_ok(self.send_button)
        self.add_cancel(self.cancel_button)
        self.plus_button = Button(160, 171, 20, 21, sprite=sm.sprites['plus_button'], callback=self.add_callback)
        self.minus_button = Button(0, 171, 20, 21, sprite=sm.sprites['minus_button'], callback=self.sub_callback)
        self.count_label = Label(30, 171, "0")
        self.add(self.plus_button)
        self.add(self.minus_button)
        self.add(self.count_label)

    def add_callback(self):
        village = self.uis.data.village
        if village.population <= self.pop + 100:
            self.pop += 100

    def sub_callback(self):
        if self.pop >= 100:
            self.pop -= 100

    def draw(self, screen):
        self.count_label.set_text(str(self.pop))
        Dialog.draw(self, screen)