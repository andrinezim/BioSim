
__author__ = 'Andrine Zimmermann, Karin Mollatt'
__email__ = 'andrine.zimmermann@nmbu.no, karin.mollatt@nmbu.no'

import pytest
from biosim.island import Island
import textwrap


class TestIsland:

    @pytest.fixture(autouse=True)
    def standard_island(self):
        """
        Fixture setting standard carnivore.

        :return: Standard carnivore class.
        """
        self.island = Island()  # skal ha to argumenter

    # Test for creating_map
    def test_creating_map(self):
        pass

    # Test for adding_population
    def test_key_error_invalid_location(self, standard_island):
        """
        Testing that we get a KeyError if the location is invalid.
        """
        island_map = """\
                   WWW
                   WLW
                   WWW"""
        island_map = textwrap.dedent(island_map)
        with pytest.raises(KeyError):
            self.island.creating_map(island_map).map_params({})

    # Test for animals_per_species
    def test_animals_per_species(self):
        pass

    # Test for find_adjacent_cell_migrate
    def find_adjacent_cell(self):
        # mocker for random choice???
        pass

    # Test for migrating_animals
    def available_landscape_migrate(self):
        pass

    # Test for restart_migration
    def test_restart_migration_to_false(self):
        pass


pytest.main(['test_island.py'])
