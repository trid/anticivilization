from building_manager import BuildingManager

__author__ = 'trid'

# I'm need it to map resources names from configs to names in village parameters
# And, yes, it's really better than use __dict__
resources_mapping = {
    'food': 'food_stockpile',
    'wood': 'wood_stockpile',
    'tree': 'wood_stockpile',
    'population': 'population',
    'food_growth': 'food_growth',
    'max_population': 'max_population',
    'wood_growth': 'wood_increasing',
    'resources_limit': 'resources_limit',
    'stone': 'stone_stockpile',
    'stone_increase': 'stone_increase',
    'iron': 'iron_stockpile',
    'iron_increase': 'iron_increase'
}

unlimited_growth = {
    'food_growth', 'max_population', 'wood_growth', 'population', 'resources_limit', 'stone_increase', 'iron_increase'
}


class Village:
    def __init__(self):
        self.population = 100
        self.population_growth = 0.01
        self.food_growth = 300
        self.food_stockpile = 100
        self.max_population = 200
        self.wood_stockpile = 0
        self.wood_increasing = 0
        self.resources_limit = 1000
        self.stone_stockpile = 0
        self.stone_increase = 0
        self.iron_stockpile = 0
        self.iron_increase = 0
        self.to_build = []

    def update(self):
        self.population += self.population * self.population_growth
        if self.population > self.max_population:
            self.population = self.max_population
        self.food_stockpile += self.food_growth
        self.food_stockpile -= self.population
        if self.food_stockpile < 0:
            self.population += self.food_stockpile
            self.food_stockpile = 0
        elif self.food_stockpile > self.resources_limit:
            self.food_stockpile = self.resources_limit
        self.wood_stockpile += self.wood_increasing
        if self.wood_stockpile > self.resources_limit:
            self.wood_stockpile = self.resources_limit
        self.stone_stockpile += self.stone_increase
        if self.stone_stockpile > self.resources_limit:
            self.stone_stockpile = self.resources_limit
        self.update_buildings()

    def get_resource_by_name(self, name):
        return resources_mapping.get(name, None)

    def change_resource_count(self, resource, count):
        resource_field = self.get_resource_by_name(resource)
        if resource is None:
            return
        stock = getattr(self, resource_field)
        stock += count
        if stock < 0:
            stock = 0
        elif stock > self.resources_limit and resource not in unlimited_growth:
            stock = self.resources_limit
        setattr(self, resource_field, stock)

    def get_resource_count(self, resource):
        resource_field = self.get_resource_by_name(resource)
        return getattr(self, resource_field)

    def remove_building(self, building):
        bm = BuildingManager()
        building_data = bm.conds[building]
        for resource in building_data.changes:
            self.change_resource_count(resource, -building_data.changes[resource])

    def add_building(self, building, tile):
        self.to_build.append((building, tile))

    def update_buildings(self):
        for b in self.to_build:
            building_name = b[0]
            tile = b[1]
            tile.building_finished = True
            building_data = BuildingManager().conds[building_name]
            for resource in building_data.changes:
                self.change_resource_count(resource, building_data.changes[resource])
        self.to_build = []