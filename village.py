__author__ = 'trid'


class Village:
    def __init__(self):
        self.population = 100
        self.population_growth = 10
        self.food_growth = 300
        self.food_stockpile = 100
        self.max_population = 200
        self.wood_stockpile = 0
        self.wood_increasing = 0

    def update(self):
        self.population += self.population_growth
        if self.population > self.max_population:
            self.population = self.max_population
        self.food_stockpile += self.food_growth
        self.food_stockpile -= self.population
        if self.food_stockpile < 0:
            self.population += self.food_stockpile
            self.food_stockpile = 0
        self.wood_stockpile += self.wood_increasing