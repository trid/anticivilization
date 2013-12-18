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
                        'cancel_button': pygame.image.load('res/images/cancel_button.png')}