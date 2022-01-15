
__author__ = 'Andrine Zimmermann, Karin Mollatt'
__email__ = 'andrine.zimmermann@nmbu.no, karin.mollatt@nmbu.no'

import pytest
from biosim.island import Island


class TestIsland:

    # Test for creating_map
    def test_creating_map(self):
        pass

    # Test for adding_population
    def test_key_error_invalid_location(self):
        pass

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
