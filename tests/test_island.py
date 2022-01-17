
__author__ = 'Andrine Zimmermann, Karin Mollatt'
__email__ = 'andrine.zimmermann@nmbu.no, karin.mollatt@nmbu.no'

from biosim.landscapes import Lowland, Highland, Desert, Water
from biosim.island import Island
import pytest


class TestIsland:

    @pytest.fixture(autouse=True)
    def standard_island(self):
        """
        Fixture setting standard island.
        """
        ini_pop = [{'loc': (3, 3),
                      'pop': [{'species': 'Herbivore',
                               'age': 5,
                               'weight': 20}
                              for _ in range(20)]},
                   {'loc': (3, 3),
                    'pop': [{'species': 'Carnivore',
                             'age': 5,
                             'weight': 20}
                            for _ in range(10)]}]
        self.standard_island = Island(ini_pop=ini_pop, island_map="WWWWW\nWWLWW\nWLLLW\nWWLWW\nWWWWW")

    # Test for creating_map
    def test_invalid_landscape(self):
        """
        Method for raising an error if the landscape is invalid.
        """
        with pytest.raises(KeyError):
            self.standard_island.creating_map(island_map="WWW\nWRW\nWWW")

    @pytest.mark.parametrize("map_string, landscape_type",
                             [["WWWWW\nWWLWW\nWLLLW\nWWLWW\nWWWWW", Lowland],
                             ["WWWWW\nWWHWW\nWHHHW\nWWHWW\nWWWWW", Highland],
                             ["WWWWW\nWWDWW\nWDDDW\nWWDWW\nWWWWW", Desert],
                             ["WWWWW\nWWWWW\nWWWWW\nWWWWW\nWWWWW", Water]])
    def test_creating_map(self, map_string, landscape_type):
        """
        Method for testing if a map is created.
        """
        obj = Island(map_string, ini_pop=[])
        cell = obj.map[(3, 3)]
        assert isinstance(cell, landscape_type)

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
    @pytest.mark.parametrize('mocker_value, new_cell',
                             [[(3, 4), (3, 4)],
                              [(3, 2), (3, 2)],
                              [(4, 3), (4, 3)],
                              [(2, 3), (2, 3)]])
    def test_find_adjacent_cell(self, mocker, mocker_value, new_cell):
        """
        Testing that finding the neighbouring cell returns the correct cell.
        """
        mocker.patch('random.choice', return_value=mocker_value)
        chosen_cell = self.standard_island.find_adjacent_cell_migrate((3, 3))
        assert chosen_cell == new_cell

    # Test for migrating_animals
    def test_migrate_to_new_cell(self, mocker):
        """
        Testing that the animal migrates to a new cell.

        Using mocker to trick the function random.random to return 0, for the migrating to happen.
        Also using it on the function random.choice, for knowing which cell it chooses.
        """
        """mocker.patch('random.random', return_value=0)
        mocker.patch('random.choice', return_value=1)
        ini_pop = len(self.standard_island.map[(3, 3)].list_herbivores) + \
                  len(self.standard_island.map[(3, 3)].list_carnivores)
        self.standard_island.migrating_animals((3, 3))
        final_pop = len(self.standard_island.map[(3, 3)].list_herbivores) + \
                    len(self.standard_island.map[(3, 3)].list_carnivores)
        assert ini_pop > final_pop"""
        pass


pytest.main(['test_island.py'])
