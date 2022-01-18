# -*- coding: utf-8 -*-

__author__ = 'Andrine Zimmermann, Karin Mollatt'
__email__ = 'andrine.zimmermann@nmbu.no, karin.mollatt@nmbu.no'

import random

"""
:mod: 'biosim.island' contains information about the annual cycle of Rossumøya. 

This file only has one class, Island. 
"""

from .landscapes import Lowland, Highland, Desert, Water


class Island:
    """
    Class for Island.
    """

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
        self.ini_pop = ini_pop
        self.map_string = island_map
        self.map_lines = island_map.splitlines()
        self.map = self.creating_map(island_map)
        self.adding_population(self.ini_pop)

        for line in self.map_lines:
            if len(line) is not len(self.map_lines[0]):
                raise ValueError(f'Each line must be of equal length.')

        for i in range(len(self.map_lines[0])):
            if self.map_lines[0][i] != 'W' or self.map_lines[-1][i] != 'W':
                raise ValueError(f'The must be surrounded of water')

        for i in range(len(self.map_lines)):
            if self.map_lines[i][0] != 'W' or self.map_lines[i][-1] != 'W':
                raise ValueError(f'The must be surrounded of water')

    def creating_map(self, island_map):
        """
        Method for creating the island map.

        :param island_map: Multi-line string specifying island geography
        :return: map_dict: Dictionary with location as key and landscape type as value.
        """

        map_dict = {}
        list_map_string = island_map.strip().split('\n')

        for line in self.map_lines:
            for landscape_type in line:
                if landscape_type not in self.map_params.keys():
                    raise ValueError('Invalid landscape type: ' + landscape_type)

        for loc_x, lines in enumerate(list_map_string):
            for loc_y, landscape_type in enumerate(lines):
                map_dict[(1 + loc_x, 1 + loc_y)] = self.map_params[landscape_type]()

        return map_dict

    @property
    def row_length(self):
        """
        Number of rows.
        """
        list_map_string = self.map_string.strip().split('\n')
        return len(list_map_string[0])

    @property
    def col_length(self):
        """
        Number of columns.
        """
        list_map_string = self.map_string.strip().split('\n')
        return len(list_map_string)

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

        amount_animals_species = {'Herbivore': amount_herbs, 'Carnivore': amount_carns}
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

    def heatmap_population(self):
        """
        Method for creating population distribution of heatmap for herbivores and carnivores.

        :return: 2D arrays with population in each cell for herbivores and carnivores.
        """
        herb_array = [[len(self.map[(row, col)].list_herbivores) for col in range(1, self.row_length+1)]
                      for row in range(1, self.col_length+1)]
        carn_array = [[len(self.map[(row, col)].list_carnivores) for col in range(1, self.row_length+1)]
                      for row in range(1, self.col_length+1)]
        return herb_array, carn_array

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
                age_list_herb.append(herb.age)

            for carn in cell.list_carnivores:
                age_list_carn.append(carn.age)

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
                weight_list_herb.append(herb.weight)

            for carn in cell.list_carnivores:
                weight_list_carn.append(carn.weight)

        return weight_list_herb, weight_list_carn

    def set_animal_params_island(self, params, species):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        for cell in self.map.values():
            cell.set_animal_params_landscapes(params, species)

    def set_landscape_params_island(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        for cell in self.map.values():
            if landscape == 'L':
                cell.set_params(params)
            elif landscape == 'H':
                cell.set_params(params)
            elif landscape == 'D':
                cell.set_params(params)
            elif landscape == 'W':
                cell.set_params(params)

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
