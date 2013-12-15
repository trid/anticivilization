from label import Label
from panel import Panel

__author__ = 'trid'

import pygame
from ui.button import Button


class UIState:
    def __init__(self, data):
        self.data = data
        self.building = None
        self.sprites = {'center': pygame.image.load('res/images/center.png'),
                        'grass': pygame.image.load('res/images/grass.png'),
                        'build_homes': pygame.image.load('res/images/build_homes.png'),
                        'build_field': pygame.image.load('res/images/build_field.png'),
                        'build_woodcutter': pygame.image.load('res/images/build_woodcutter.png'),
                        'send_expedition': pygame.image.load('res/images/send_expedition.png'),
                        'houses': pygame.image.load('res/images/houses.png'),
                        'field': pygame.image.load('res/images/field.png'),
                        'human': pygame.image.load('res/images/human.png'),
                        'tree': pygame.image.load('res/images/tree.png'),
                        'woodcutter': pygame.image.load('res/images/woodcutter.png'),
                        'monster': pygame.image.load('res/images/monster.png'),
                        'statistics_button': pygame.image.load('res/images/statistics_button.png'),
                        'specialists_button': pygame.image.load('res/images/specialists_button.png')}
        self.button_homes = Button(0, 0, 115, 23, 'build_homes')
        self.button_fields = Button(0, 0, 93, 23, 'build_field')
        self.button_woodcutter = Button(0, 0, 140, 21, 'build_woodcutter')
        self.button_expedition = Button(0, 0, 132, 21, 'send_expedition')
        self.button_statistics = Button(600, 579, 100, 21, sprite=self.sprites['statistics_button'], callback=self.show_statistics)
        self.button_specialists = Button(700, 579, 100, 21, sprite=self.sprites['specialists_button'], callback=self.show_specialists)
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
            screen.blit(self.sprites[button.name], (button.x, button.y))

    def process_popup(self, x, y):
        for button in self.button_set:
            button.is_pressed(x, y)

    def update_labels(self):
        self.population_label.set_text("Population: %d(+%d)" % (self.data.village.population, self.data.village.population_growth))
        self.food_label.set_text("Food: %d(+%d)" % (self.data.village.food_stockpile, self.data.village.food_growth))
        self.wood_label.set_text("Wood: %d(+%d)" % (self.data.village.wood_stockpile, self.data.village.wood_increasing))

    def draw(self, screen):
        for item in self.ui_items:
            item.draw(screen)

    def show_specialists(self):
        self.specialists_panel.visible = True
        self.status_panel.visible = False

    def show_statistics(self):
        self.specialists_panel.visible = False
        self.status_panel.visible = True

    def process_clicks(self, x, y):
        result = False
        for button in self.clickables:
            result = result or button.is_pressed(x, y)
        return result