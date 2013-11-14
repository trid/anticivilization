__author__ = 'trid'


class Village:
    def __init__(self):
        self.population = 100
        self.population_growth = 10
        self.food = 100
        self.max_population = 200

    def update_pop(self):
        self.population += self.population_growth
        if self.population > self.max_population:
            self.population = self.max_population