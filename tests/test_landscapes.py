
__author__ = 'Andrine Zimmermann, Karin Mollatt'
__email__ = 'andrine.zimmermann@nmbu.no, karin.mollatt@nmbu.no'

import pytest
from biosim.landscapes import Lowland, Highland, Desert, Water


@pytest.mark.parametrize('class_to_test', [Lowland, Highland, Desert, Water])
class TestLandscapes:
    """
    Class for testing the landscapes superclass.
    """
    pop_h = [{'species': 'Herbivore',
             'age': 5,
              'weight': 20}
             for _ in range(50)]

    # Tests for set_params method.
    def test_negative_param_value(self, class_to_test):
        """
        Testing that we get a ValueError if the parameters are negative.

        :param class_to_test: Lowland, Highland, Desert and Water subclasses
        """
        obj = class_to_test()
        pass

    def test_param_update(self, class_to_test):
        """
        Testing if the default params are updating.

        :param class_to_test: Lowland, Highland, Desert and Water subclasses
        """
        obj = class_to_test()
        pass

    def test_invalid_param_name(self, class_to_test):
        """
        Testing that we get a ValueError if the parameter name is wrong.

        :param class_to_test: Lowland, Highland, Desert and Water subclasses.
        """
        obj = class_to_test()
        pass

    # Test for animals_population
    def test_invalid_species_name(self, class_to_test):
        """
        Testing that we get a TypeError if the correct name of the species is not given.

        :param class_to_test: Lowland, Highland, Desert and Water subclasses.
        """
        obj = class_to_test()
        pass

    # Test for feeding_herbs
    def test_amount_fodder_available(self, class_to_test):
        """
        Testing that the amount of fodder available decreases by the amount of fodder that
        is eaten.

        :param class_to_test: Lowland, Highland, Desert and Water subclasses.
        """
        obj = class_to_test()
        pass

    # Test for feeding_carn_with_herbs.
    def test_herbs_get_eaten(self, class_to_test):
        """
        Testing that the eaten herbivores are removed from the list of present herbivores.

        :param class_to_test: Lowland, Highland, Desert and Water subclasses.
        """
        obj = class_to_test()
        obj.animals_population(self.pop_h)
        ini_list_herb = obj.list_herbivores
        obj.feeding_carn_with_herbs()
        assert len(obj.list_herbivores) < len(ini_list_herb)

    # Test for animal_gives_birth
    # Nødvendig test????
    def test_animals_get_born(self, class_to_test):
        """
        Testing that the newborn are added to the population in the cell.

        :param class_to_test: Lowland, Highland, Desert and Water subclasses
        """
        obj = class_to_test()
        pass

    # Test for animal_dies
    def test_animals_die(self, class_to_test):
        """
        Testing that the animal is removed from the rest of population if it dies.

        :param class_to_test: Lowland, Highland, Desert and Water subclasses
        """
        obj = class_to_test()
        pass

    # Test for distribute_migrated_animals
    def test_distribute_migrated_animals(self, class_to_test):
        """


        :param class_to_test: Lowland, Highland, Desert and Water subclasses
        :return:
        """
        pass

    # Test for annual_restart_migration
    def test_has_migrated_is_false(self, class_to_test):
        """

        :param class_to_test: Lowland, Highland, Desert and Water subclasses
        :return:
        """


class TestLowland:

    # Test for grow_fodder
    def test_fodder_regrows_update(self):
        """
        Testing that the correct parameter is given for fodder available.

        :return:
        """
        pass


class TestHighland:

    # Test for grow_fodder
    def test_fodder_regrows_update(self):
        """
        Testing that the correct parameter is given for fodder available.

        :return:
        """
        pass


class TestDesert:

    # Test for grow_fodder
    def test_fodder_regrows_update(self):
        """
        Testing that the correct parameter is given for fodder available.

        :return:
        """
        pass


class TestWater:

    # Test for grow_fodder
    def test_fodder_regrows_update(self):
        """
        Testing that the correct parameter is given for fodder available.

        :return:
        """
        pass


pytest.main(['test_landscapes.py'])
