
__author__ = 'Andrine Zimmermann, Karin Mollatt'
__email__ = 'andrine.zimmermann@nmbu.no, karin.mollatt@nmbu.no'

import pytest
from biosim.island import Island
from biosim.landscapes import Lowland


class TestIsland:

    @pytest.fixture(autouse=True)
    def standard_island(self):
        """
        Fixture setting standard island.

        :return: Standard island class.
        """
        ini_herbs = [{'loc': (3, 3),
                      'pop': [{'species': 'Herbivore',
                               'age': 5,
                               'weight': 20}
                              for _ in range(20)]}]
        self.standard_island = Island(ini_pop=ini_herbs, island_map="WWWWW\nWWLWW\nWLLLW\nWWLWW\nWWWWW")

    # Test for creating_map
    def test_invalid_landscape(self):
        """
        Method for raising an error if the landscape is invalid.
        """
        """with pytest.raises(ValueError):
            self.standard_island.creating_map(island_map="WWW\nWRW\nWWW")"""
        pass

    def test_creating_map(self):
        """
        Method for testing if a map is created.
        """
        """island_map_string = "WWWWW\nWWLWW\nWLLLW\nWWLWW\nWWWWW"
        self.standard_island.creating_map(island_map_string)
        key_list = self.standard_island.map.keys()
        assert self.standard_island.map[(3, 3)] == type()"""

    # Test for adding_population
    def test_key_error_invalid_location(self):
        """
        Testing that we get a KeyError if the location is invalid.
        """
        invalid_loc_pop = [{'loc': (0, 0),
                            'pop': [{'species': 'Herbivore',
                                     'age': 5,
                                     'weight': 20}
                                    for _ in range(20)]}]
        with pytest.raises(KeyError):
            Island(ini_pop=invalid_loc_pop, island_map="WWWWW\nWWLWW\nWLLLW\nWWLWW\nWWWWW")

    # Test for find_adjacent_cell_migrate
    def find_adjacent_cell(self):
        # mocker for random choice???
        pass

    # Test for migrating_animals
    def available_landscape_migrate(self):
        """
        Testing that if the landscape is available, it is possib
        :return:
        """
        pass


pytest.main(['test_island.py'])
