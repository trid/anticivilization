import pygame

__author__ = 'TriD'


class SpriteManager(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SpriteManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.sprites = {'center': pygame.image.load('res/images/center.png'),
                        'grass': pygame.image.load('res/images/grass.png'),
                        'water': pygame.image.load('res/images/water.png'),
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
                        'specialists_button': pygame.image.load('res/images/specialists_button.png'),
                        'warrior_button': pygame.image.load('res/images/warrior_button.png'),
                        'worker_button': pygame.image.load('res/images/worker_button.png'),
                        'create_sp_button': pygame.image.load('res/images/create_specialist_button.png'),
                        'up_button': pygame.image.load('res/images/up_button.png'),
                        'down_button': pygame.image.load('res/images/down_button.png'),
                        'send_expedition_ok': pygame.image.load('res/images/send_expedition_ok.png'),
                        'cancel_button': pygame.image.load('res/images/cancel_button.png'),
                        'road': pygame.image.load('res/images/stone_road.png'),
                        'build_road': pygame.image.load('res/images/build_road.png'),
                        'port': pygame.image.load('res/images/port.png'),
                        'build_port': pygame.image.load('res/images/build_port.png'),
                        'stockpile': pygame.image.load('res/images/stockpile.png'),
                        'build_stockpile': pygame.image.load('res/images/build_stockpile.png'),
                        'boat': pygame.image.load('res/images/boat.png'),
                        'save_button': pygame.image.load('res/images/save_button.png'),
                        'load_button': pygame.image.load('res/images/load_button.png'),
                        'plus_button': pygame.image.load('res/images/plus_button.png'),
                        'minus_button': pygame.image.load('res/images/minus_button.png'),
                        'stone': pygame.image.load('res/images/stone_resource.png'),
                        'port_expedition_button': pygame.image.load('res/images/port_expedition_button.png'),
                        'build_button': pygame.image.load('res/images/build_button.png'),
                        'iron': pygame.image.load('res/images/iron.png'),
                        'stone_carrier': pygame.image.load('res/images/stone_carrier.png'),
                        'build_stone_carrier': pygame.image.load('res/images/build_stone_carrier.png'),
                        'info_button': pygame.image.load('res/images/button_info.png'),
                        'resources_button': pygame.image.load('res/images/resources_button.png'),
                        'monster_button': pygame.image.load('res/images/monster_button.png'),
                        'build_workshop': pygame.image.load('res/images/build_workshop.png'),
                        'workshop': pygame.image.load('res/images/workshop.png'),
                        'destruct': pygame.image.load('res/images/destruct_building.png'),
                        'repeat_button': pygame.image.load('res/images/repeat_button.png'),
                        'protect_button': pygame.image.load('res/images/button_protect.png'),
                        'remaining': pygame.image.load('res/images/bone_resource.png'),
                        'end_turn_button': pygame.image.load('res/images/end_turn_button.png'),
                        'spells_button': pygame.image.load('res/images/spells_button.png'),
                        'build_iron_mine': pygame.image.load('res/images/build_iron_mine.png'),
                        'iron_mine': pygame.image.load('res/images/mine.png'),
                        'new_game_button': pygame.image.load('res/images/button_new_game.png'),
                        'exit_button': pygame.image.load('res/images/button_exit.png'),
                        }