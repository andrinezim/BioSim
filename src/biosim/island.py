
__author__ = 'Andrine Zimmermann, Karin Mollatt'
__email__ = 'andrine.zimmermann@nmbu.no, karin.mollatt@nmbu.no'

import random

"""
Module for island. 
"""

from .landscapes import Lowland, Highland, Desert, Water


class Island:

    map_params = {'L': Lowland,
                  'H': Highland,
                  'D': Desert,
                  'W': Water}

    def __init__(self, island_map, ini_pop):
        """
        Method for saving values in class.

        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        """

        # Defining the value for amount of years to use.
        self.amount_years = 0

        self.ini_pop = ini_pop
        self.map = self.creating_map(island_map)
        self.adding_population(self.ini_pop)

    def creating_map(self, island_map):
        """
        Method for creating the island map.

        :param island_map: Multi-line string specifying island geography
        :return: map_dict: Dictionary with location as key and landscape type as value.
        """

        map_dict = {}
        list_map_string = island_map.strip().split('\n')

        for loc_x, lines in enumerate(list_map_string):
            for loc_y, landscape_type in enumerate(lines):
                map_dict[(1 + loc_x, 1 + loc_y)] = self.map_params[landscape_type]()

        return map_dict

    def adding_population(self, incoming_pop=None):
        """
        Method for adding population to the island.

        :param incoming_pop: List of dictionaries specifying initial population
        """
        if incoming_pop is None:
            return
        else:
            current_pop = incoming_pop

        for dict_loc_pop in current_pop:
            loc = dict_loc_pop['loc']
            if loc not in self.map:
                raise KeyError('This location is invalid.')

            pop = dict_loc_pop['pop']
            self.map[loc].animals_population(pop)

    def animals_per_species(self):
        """
        Method for creating a dictionary containing the amount of animals per species.

        :return: Dictionary with the amount of animals per species.
        """
        amount_herbs = 0
        amount_carns = 0

        for cell in self.map:
            if self.map[cell].available:
                herb_list = self.map[cell].list_herbivores
                carn_list = self.map[cell].list_carnivores
                amount_herbs += len(herb_list)
                amount_carns += len(carn_list)

        amount_animals_species = {'Herbivores': amount_herbs, 'Carnivores': amount_carns}
        total_amount_animals = amount_herbs + amount_carns
        return amount_animals_species, total_amount_animals

    @staticmethod
    def find_adjacent_cell_migrate(cell):
        """
        Method for finding the neighbouring cells, and deciding which cell to migrate to.

        :return: The cell to be migrated to.
        """
        x_loc, y_loc = cell

        north_loc = (x_loc, y_loc + 1)
        south_loc = (x_loc, y_loc - 1)
        east_loc = (x_loc + 1, y_loc)
        west_loc = (x_loc - 1, y_loc)

        loc_list = [north_loc, south_loc, east_loc, west_loc]

        selected_cell = random.choice(loc_list)
        return selected_cell

    def migrating_animals(self, cell):
        """
        Method for migrating animals.

        Ensures that the cell is an available landscape type. Water is the only unavailable landscape.
        Puts the migrating animals in a new cell (location), and adds the animal to the population in that
        cell. Also makes sure that the animal is removed from the population to the previous cell.

        :param cell: Location tuple
        """
        moved_herbs = []
        moved_carns = []

        if self.map[cell].available is True:
            migrated_herbs, migrated_carns = self.map[cell].distribute_migrated_animals()

            for herb in migrated_herbs:
                next_loc = self.find_adjacent_cell_migrate(cell)
                if self.map[next_loc].available is False:
                    break
                else:
                    self.map[next_loc].add_single_animal(herb)
                    herb.has_migrated = True
                    moved_herbs.append(herb)

            self.map[cell].list_herbivores = [herb for herb in self.map[cell].list_herbivores
                                              if herb not in moved_herbs]

            for carn in migrated_carns:
                next_loc = self.find_adjacent_cell_migrate(cell)
                if self.map[next_loc].available is False:
                    break
                else:
                    self.map[next_loc].add_single_animal(carn)
                    carn.has_migrated = True
                    moved_carns.append(carn)

            self.map[cell].list_carnivores = [carn for carn in self.map[cell].list_carnivores
                                              if carn not in moved_carns]

    def restart_migration(self):
        """
        Method for setting has_migrated attribute back to False at the end of the year.

        An animal can only migrate once each year.
        """
        for cell in self.map:
            self.map[cell].annual_restart_migration()

    def fitness_list(self):
        """
        Method for creating list with fitness for all animals.

        :return: Lists containing fitness for herbivores and carnivores.
        """
        fitness_list_herb = []
        fitness_list_carn = []

        for cell in self.map.values():
            for herb in cell.list_herbivores:
                fitness_list_herb.append(herb.phi)

        for cell in self.map.values():
            for carn in cell.list_carnivores:
                fitness_list_carn.append(carn.phi)

        return fitness_list_herb, fitness_list_carn

    def age_list(self):
        """
        Method for creating list with ages for all animals.

        :return: Lists containing fitness for herbivores and carnivores.
        """
        age_list_herb = []
        age_list_carn = []

        for cell in self.map.values():
            for herb in cell.list_herbivores:
                age_list_herb.append(herb.phi)

        for cell in self.map.values():
            for carn in cell.list_carnivores:
                age_list_carn.append(carn.phi)

        return age_list_herb, age_list_carn

    def weight_list(self):
        """
        Method for creating list with weights for all animals.

        :return: Lists containing fitness for herbivores and carnivores.
        """
        weight_list_herb = []
        weight_list_carn = []

        for cell in self.map.values():
            for herb in cell.list_herbivores:
                weight_list_herb.append(herb.phi)

        for cell in self.map.values():
            for carn in cell.list_carnivores:
                weight_list_carn.append(carn.phi)

        return weight_list_herb, weight_list_carn

    def annual_cycle_simulation(self):
        """
        Method for simulating one year one the island. It follows the annual cycle.
        """
        for cell in self.map:
            self.map[cell].eating_process()
            self.map[cell].animal_gives_birth()
            self.migrating_animals(cell)
            self.map[cell].animal_gets_older()
            self.map[cell].animal_dies()

        self.restart_migration()
