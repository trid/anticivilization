from expedition import Expedition
from label import Label
from monster import Monster
from panel import Panel
from point import Point
from specialist import Specialist
import specialist
from sprite_manager import SpriteManager
from ui.clickable_specialists_list import ClickableSpList
from ui.dialog import Dialog
from ui.specialist_panel import SpecialistPanel
from ui.specialists_list import SpecialistsList
from ui.pop_up_menu import PopUpMenu

__author__ = 'trid'

import pygame
from ui.button import Button


class UIState(object):
    def __init__(self, data):
        self.data = data
        self.building = None

        self.button_homes = Button(0, 0, 115, 23, sprite=SpriteManager().sprites['build_homes'])
        self.button_fields = Button(0, 0, 93, 23, sprite=SpriteManager().sprites['build_field'])
        self.button_woodcutter = Button(0, 0, 140, 21, sprite=SpriteManager().sprites['build_woodcutter'])
        self.button_road = Button(0, 0, 92, 21, sprite=SpriteManager().sprites['build_road'])
        self.button_port = Button(0, 0, 92, 21, sprite=SpriteManager().sprites['build_port'])
        self.button_stockpile = Button(0, 0, 132, 21, sprite=SpriteManager().sprites['build_stockpile'])
        self.button_stone_carrier = Button(0, 0, 164, 21, sprite=SpriteManager().sprites['build_stone_carrier'])
        self.button_expedition = Button(0, 0, 132, 21, sprite=SpriteManager().sprites['send_expedition'], callback=self.on_send_expedition_click)
        self.button_statistics = Button(600, 579, 100, 21, sprite=SpriteManager().sprites['statistics_button'], callback=self.show_statistics)
        self.button_specialists = Button(700, 579, 100, 21, sprite=SpriteManager().sprites['specialists_button'], callback=self.show_specialists)
        self.button_info = Button(0, 0, 44, 21, sprite=SpriteManager().sprites['info_button'])
        self.exp_click_pos = None
        self.population_label = Label(600, 0, "")
        self.food_label = Label(600, 20, "")
        self.wood_label = Label(600, 40, "")
        self.stone_label = Label(600, 60, "")
        #Ok, here we shall store ui items, for have less writing about how to draw them
        self.ui_items = []
        self.status_panel = Panel()
        self.status_panel.add(self.population_label)
        self.status_panel.add(self.food_label)
        self.status_panel.add(self.wood_label)
        self.status_panel.add(self.stone_label)
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
        self.create_chose_specialists_dialog()
        self.create_main_menu_dialog()
        self.create_resource_or_monster_dialog()
        self.expedition_people_count = 0
        self.build_button = Button(0, 0, 51, 23, callback=self.show_buildings_pop_up, sprite=SpriteManager().sprites['build_button'])
        self.ui_items.append(self.build_button)
        self.clickables.append(self.build_button)
        self.generate_building_menu()
        self.map_popup = PopUpMenu()
        self.ui_items.append(self.map_popup)
        self.pop_up = None

    def update_labels(self):
        self.population_label.set_text("Population: %d(+%d)" % (self.data.village.population, self.data.village.population_growth))
        self.food_label.set_text("Food: %d(+%d)" % (self.data.village.food_stockpile, self.data.village.food_growth))
        self.wood_label.set_text("Wood: %d(+%d)" % (self.data.village.wood_stockpile, self.data.village.wood_increasing))
        self.stone_label.set_text("Stone: %d(+%d)" % (self.data.village.stone_stockpile, self.data.village.stone_increase))

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
        if self.pop_up and self.pop_up.visible:
            result = result or self.pop_up.is_pressed(x, y)
            self.pop_up.hide()
        for button in self.clickables:
            result = result or button.is_pressed(x, y)
            if result:
                return True
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
        if self.data.village.population > 1000 * len(self.data.specialists):
            self.dialog = self.add_sp_dialog

    def create_chose_specialists_dialog(self):
        dialog = Dialog(400, 200, 200, 300)
        sp_list = ClickableSpList(self.data, 0, 0)
        dialog.add(sp_list)
        send_button = Button(0, 271, 44, 21, sprite=SpriteManager().sprites['send_expedition_ok'], callback=self.send_expedition)
        cancel_button = Button(100, 271, 60, 21, sprite=SpriteManager().sprites['cancel_button'], callback=self.dialog_cancel_button)
        dialog.add_ok(send_button)
        dialog.add_cancel(cancel_button)
        plus_button = Button(160, 171, 20, 21, sprite=SpriteManager().sprites['plus_button'], callback=self.add_people)
        minus_button = Button(0, 171, 20, 21, sprite=SpriteManager().sprites['minus_button'], callback=self.remove_people)
        self.count_label = Label(30, 171, "0")
        dialog.add(plus_button)
        dialog.add(minus_button)
        dialog.add(self.count_label)
        self.cl_sp_list = sp_list
        self.chose_sp_dialog = dialog

    def on_send_expedition_click(self):
        tile = self.data.game_map[self.exp_click_pos.x][self.exp_click_pos.y]
        if isinstance(tile.unit, Monster) and tile.resource:
            self.dialog = self.resource_or_monster_dialog
        else:
            self.show_chose_specialists_dialog()

    def show_chose_specialists_dialog(self):
        self.expedition_people_count = 0
        self.cl_sp_list.reset()
        self.dialog = self.chose_sp_dialog

    def dialog_cancel_button(self):
        self.hide_dialog()

    def send_expedition(self):
        if self.expedition_people_count <= 0:
            return
        self.hide_dialog()
        if self.cl_sp_list.chosen and self.data.village.food_stockpile > 100:
            expedition = Expedition(self.cl_sp_list.chosen, self.data.center, self.expedition_people_count)
            expedition.find_path(self.data.center.x, self.data.center.y, self.exp_click_pos.x, self.exp_click_pos.y, self.data.game_map)
            self.data.expeditions.append(expedition)
            self.data.village.food_stockpile -= 100

    def create_main_menu_dialog(self):
        self.main_menu = Dialog(300, 150, 200, 300)
        esc_button = Button(0, 0, 0, 0, callback=self.hide_dialog)
        self.main_menu.add_cancel(esc_button)
        save_button = Button(78, 0, 44, 21, sprite=SpriteManager().sprites['save_button'], callback=self.save_game)
        load_button = Button(78, 24, 44, 21, sprite=SpriteManager().sprites['load_button'], callback=self.load_game)
        self.main_menu.add(save_button)
        self.main_menu.add(load_button)

    def hide_dialog(self):
        self.dialog = None

    def save_game(self):
        self.data.save('save')

    def load_game(self):
        self.data.load('save')

    def add_people(self):
        new_count = self.expedition_people_count + 100
        if new_count < self.data.village.population:
            self.expedition_people_count = new_count
            self.count_label.set_text(str(self.expedition_people_count))

    def remove_people(self):
        new_count = self.expedition_people_count - 100
        if new_count > 0:
            self.expedition_people_count = new_count
            self.count_label.set_text(str(self.expedition_people_count))

    def generate_building_menu(self):
        self.building_popup = PopUpMenu()
        self.building_popup.add_item(self.button_homes)
        self.building_popup.add_item(self.button_fields)
        self.building_popup.add_item(self.button_road)
        self.building_popup.add_item(self.button_woodcutter)
        self.building_popup.add_item(self.button_port)
        self.building_popup.add_item(self.button_stockpile)
        self.building_popup.add_item(self.button_stone_carrier)
        self.ui_items.append(self.building_popup)

    def show_buildings_pop_up(self):
        self.building_popup.show(0, 0)
        self.pop_up = self.building_popup

    def show_map_popup(self, mouse_x, mouse_y, tile):
        self.map_popup.clean()
        self.map_popup.add_item(self.button_info)
        if tile.resource or isinstance(tile.unit, Monster):
            self.map_popup.add_item(self.button_expedition)
            self.exp_click_pos = Point((mouse_x + self.data.dx) / 32, (mouse_y + self.data.dy) / 32)
        self.pop_up = self.map_popup
        self.pop_up.show(mouse_x, mouse_y)

    def create_resource_or_monster_dialog(self):
        self.resource_or_monster_dialog = Dialog(325, 285, 150, 30)
        resource_button = Button(0, 5, 84, 21, sprite=SpriteManager().sprites['resources_button'], callback=self.show_chose_specialists_dialog)
        monster_button = Button(85, 5, 68, 21, sprite=SpriteManager().sprites['monster_button'])
        self.resource_or_monster_dialog.add(resource_button)
        self.resource_or_monster_dialog.add(monster_button)