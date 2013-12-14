__author__ = 'TriD'

CHIEFTAIN = 1
WARRIOR = 2
WORKER = 3


class Specialist():
    def __init__(self, s_type):
        self.s_type = s_type
        self.experience = 0
        self.level_up_exp = 100
        self.level = 1
        self.occupied = False

    def add_exp(self, exp):
        self.experience += exp
        if self.experience >= self.level_up_exp:
            self.level += 1
            self.level_up_exp = 100 * (self.level ** 2)