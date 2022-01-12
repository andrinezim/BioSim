
__author__ = 'Andrine Zimmermann, Karin Mollatt'
__email__ = 'andrine.zimmermann@nmbu.no, karin.mollatt@nmbu.no'

import random

"""
Module for island. 
"""

from .landscapes import Lowland, Highland, Desert, Water


class Island:

    map_params = {"L": Lowland,
                  "H": Highland,
                  "D": Desert,
                  "W": Water}

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

        loc_x = 1
        for line in list_map_string:
            loc_y = 1
            for landscape_type in line:
                map_dict[(loc_x, loc_y)] = self.map_params[landscape_type]()
                loc_y += 1
            loc_x += 1

        return map_dict

    def adding_population(self, incoming_pop=None):
        """
        Method for adding population to the island.

        :param incoming_pop: List of dictionaries specifying initial population
        :return:
        """
        if incoming_pop is None:
            return
        else:
            current_pop = incoming_pop

        for dict_loc_pop in current_pop:
            loc = dict_loc_pop['loc']

            pop = dict_loc_pop['pop']
            self.map[loc].animals_population(pop)

    # @staticmethod
    def find_adjacent_cell_migrate(self, cell):
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
        if self.map[cell].available is True:
            migrated_herbs, migrated_carns = self.map[cell].distribute_migrated_animals()
            for herb in migrated_herbs:
                next_loc = self.find_adjacent_cell_migrate(cell)
                if self.map[next_loc].available is False:
                    break
                else:
                    self.map[next_loc].adding_population(herb)
                    herb.has_migrated = True
                    # Remove from list.


    def annual_cycle_simulation(self):
        """
        Method for simulating one year one the island. It follows the annual cycle.

        :return:
        """

        # return number of animals per species
        pass
