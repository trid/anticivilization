from label import Label
from panel import Panel
from specialist import Specialist
import specialist
from sprite_manager import SpriteManager
from ui.dialog import Dialog
from ui.specialist_panel import SpecialistPanel
from ui.specialists_list import SpecialistsList

__author__ = 'trid'

import pygame
from ui.button import Button


class UIState(object):
    def __init__(self, data):
        self.data = data
        self.building = None

        self.button_homes = Button(0, 0, 115, 23, 'build_homes')
        self.button_fields = Button(0, 0, 93, 23, 'build_field')
        self.button_woodcutter = Button(0, 0, 140, 21, 'build_woodcutter')
        self.button_expedition = Button(0, 0, 132, 21, 'send_expedition')
        self.button_statistics = Button(600, 579, 100, 21, sprite=SpriteManager().sprites['statistics_button'], callback=self.show_statistics)
        self.button_specialists = Button(700, 579, 100, 21, sprite=SpriteManager().sprites['specialists_button'], callback=self.show_specialists)
        self.grass_click_buttons = [self.button_homes, self.button_fields, self.button_woodcutter]
        self.resource_click_buttons = self.grass_click_buttons + [self.button_expedition]
        self.button_set = None
        self.exp_click_pos = None
        self.population_label = Label(600, 0, "")
        self.food_label = Label(600, 20, "")
        self.wood_label = Label(600, 40, "")
        #Ok, here we shall store ui items, for have less writing about how to draw them
        self.ui_items = []
        self.status_panel = Panel()
        self.status_panel.add(self.population_label)
        self.status_panel.add(self.food_label)
        self.status_panel.add(self.wood_label)
        self.ui_items.append(self.status_panel)
        self.ui_items.append(self.button_statistics)
        self.ui_items.append(self.button_specialists)
        self.specialists_panel = Panel()
        self.specialists_panel.visible = False
        self.ui_items.append(self.specialists_panel)
        self.dialog = None
        self.clickables = []
        self.clickables.append(self.button_specialists)
        self.clickables.append(self.button_statistics)
        self.clickables.append(self.specialists_panel)
        #Yeah it's fucking looooong initialization
        self.create_specialist_button = Button(600, 558, 148, 21, callback=self.show_create_specialist_dialog, sprite=SpriteManager().sprites['create_sp_button'])
        self.specialists_panel.add(self.create_specialist_button)
        self.create_chose_specialist_type_dialog()
        self.sp_list_panel = SpecialistsList(self.data, 600, 0)
        self.specialists_panel.add(self.sp_list_panel)

    def setup_buttons(self, x, y):
        self.button_homes.x = x
        self.button_homes.y = y
        self.button_fields.x = x
        self.button_fields.y = y + 23
        self.button_woodcutter.x = x
        self.button_woodcutter.y = y + 46
        self.button_expedition.x = x
        self.button_expedition.y = y + 67

    def set_grass_click(self):
        self.button_set = self.grass_click_buttons

    def set_resource_click_buttons(self):
        self.button_set = self.resource_click_buttons

    def draw_buttons(self, screen):
        y = self.button_homes.y
        for button in self.button_set:
            screen.blit(SpriteManager().sprites[button.name], (button.x, button.y))

    def process_popup(self, x, y):
        for button in self.button_set:
            button.is_pressed(x, y)

    def update_labels(self):
        self.population_label.set_text("Population: %d(+%d)" % (self.data.village.population, self.data.village.population_growth))
        self.food_label.set_text("Food: %d(+%d)" % (self.data.village.food_stockpile, self.data.village.food_growth))
        self.wood_label.set_text("Wood: %d(+%d)" % (self.data.village.wood_stockpile, self.data.village.wood_increasing))

    def draw(self, screen):
        if self.dialog:
            self.dialog.draw(screen)
        for item in self.ui_items:
            item.draw(screen)

    def show_specialists(self):
        self.specialists_panel.visible = True
        self.status_panel.visible = False

    def show_statistics(self):
        self.specialists_panel.visible = False
        self.status_panel.visible = True

    def process_clicks(self, x, y):
        if self.dialog:
            self.dialog.click(x, y)
            return True
        result = False
        for button in self.clickables:
            result = result or button.is_pressed(x, y)
        return result

    def add_warrior(self):
        self.dialog = None
        self.data.specialists.append(Specialist(specialist.WARRIOR))
        self.sp_list_panel.update_specialists()

    def add_worker(self):
        self.dialog = None
        self.data.specialists.append(Specialist(specialist.WORKER))
        self.sp_list_panel.update_specialists()

    def create_chose_specialist_type_dialog(self):
        dialog = Dialog(350, 275, 200, 50)
        warrior_button = Button(0, 14, 61, 21, sprite=SpriteManager().sprites['warrior_button'], callback=self.add_warrior)
        worker_button = Button(100, 14, 60, 21, sprite=SpriteManager().sprites['worker_button'], callback=self.add_worker)
        dialog.add(warrior_button)
        dialog.add(worker_button)
        self.add_sp_dialog = dialog

    def show_create_specialist_dialog(self):
        self.dialog = self.add_sp_dialog