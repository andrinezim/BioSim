
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
        with pytest.raises(ValueError):
            obj.set_params({'f_max': -3})

    def test_param_update(self, class_to_test):
        """
        Testing if the default params are updating.

        :param class_to_test: Lowland, Highland, Desert and Water subclasses
        """
        obj = class_to_test()
        new_params = {'f_max': 300}
        current_params = obj.set_params(new_params)
        assert current_params != new_params

    def test_invalid_param_name(self, class_to_test):
        """
        Testing that we get a ValueError if the parameter name is wrong.

        :param class_to_test: Lowland, Highland, Desert and Water subclasses.
        """
        obj = class_to_test()
        with pytest.raises(ValueError):
            obj.set_params({'fodder': 10})

    # Test for animals_population
    def test_invalid_species_name(self, class_to_test):
        """
        Testing that we get a TypeError if the correct name of the species is not given.

        :param class_to_test: Lowland, Highland, Desert and Water subclasses.
        """
        obj = class_to_test()
        invalid_list = [{'species': 'Lion',
                         'age': 5,
                         'weight': 20}
                        for _ in range(10)]
        with pytest.raises(TypeError):
            obj.animals_population(invalid_list)

    # Test for feeding_herbs
    def test_amount_fodder_available(self, class_to_test):
        """
        Testing that the amount of fodder available decreases by the amount of fodder that
        is eaten.

        :param class_to_test: Lowland, Highland, Desert and Water subclasses.
        """
        obj = class_to_test()
        obj.params_fodder = 15
        obj.feeding_herbs()
        assert obj.feeding_herbs == 5

    # Test for feeding_carn_with_herbs.
    def test_herbs_get_eaten(self, class_to_test):
        """
        Testing that the eaten herbivores are removed from the list of present herbivores.

        :param class_to_test: Lowland, Highland, Desert and Water subclasses.
        """
        obj = class_to_test()
        herb_list = [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(10)]
        carn_list = [{'species': 'Carnivore',
                      'age': 5,
                      'weight': 20}
                     for _ in range(10)]
        obj.animals_population(herb_list + carn_list)
        # ini_list_herb = obj.list_herbivores
        obj.feeding_carn_with_herbs()
        assert len(obj.list_herbivores) < len(obj.list_carnivores)

    # Test for animal_gives_birth
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
        pass


class TestLowland:

    @pytest.fixture
    def standard_lowland(self):
        """
        Fixture setting standard lowland.

        :return: Standard lowland class.
        """
        self.standard_lowland = Lowland()

    # Test for grow_fodder
    def test_fodder_regrows_update(self, standard_lowland):
        """
        Testing that the correct parameter is given for fodder available.
        """
        self.standard_lowland.grow_fodder()
        assert self.standard_lowland.amount_fodder == self.standard_lowland.params_fodder['f_max']


class TestHighland:

    @pytest.fixture(autouse=True)
    def standard_highland(self):
        """
        Fixture setting standard highland.

        :return: Standard highland class.
        """
        self.standard_highland = Highland()

    # Test for grow_fodder
    def test_fodder_regrows_update(self):
        """
        Testing that the correct parameter is given for fodder available.
        """
        self.standard_highland.grow_fodder()
        assert self.standard_highland.amount_fodder == self.standard_highland.params_fodder['f_max']


class TestDesert:

    @pytest.fixture(autouse=True)
    def standard_desert(self):
        """
        Fixture setting standard desert.

        :return: Standard desert class.
        """
        self.standard_desert = Desert()

    # Test for grow_fodder
    def test_fodder_regrows_update(self):
        """
        Testing that the correct parameter is given for fodder available.
        """
        self.standard_desert.grow_fodder()
        assert self.standard_desert.amount_fodder == self.standard_desert.params_fodder['f_max']


class TestWater:

    @pytest.fixture(autouse=True)
    def standard_water(self):
        """
        Fixture setting standard water.

        :return: Standard water class.
        """
        self.standard_water = Water()

    # Test for grow_fodder
    def test_fodder_regrows_update(self):
        """
        Testing that the correct parameter is given for fodder available.
        """
        self.standard_water.grow_fodder()
        assert self.standard_water.amount_fodder == self.standard_water.params_fodder['f_max']


pytest.main(['test_landscapes.py'])
