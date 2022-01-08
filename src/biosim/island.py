
__author__ = 'Andrine Zimmermann, Karin Mollatt'
__email__ = 'andrine.zimmermann@nmbu.no, karin.mollatt@nmbu.no'

"""
Module for island. 
"""

from biosim.landscapes import Lowland


class Island:

    map_params = {'L': Lowland}

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
            current_pop = self.ini_pop
        else:
            current_pop = incoming_pop

        for dict_loc_pop in current_pop:
            loc = dict_loc_pop['loc']

            pop = dict_loc_pop['pop']
            self.map[loc].animals_population(pop)

    def annual_cycle_simulation(self):
        """
        Method for simulating one year one the island. It follows the annual cycle.

        :return:
        """

        # return number of animals per species
        pass