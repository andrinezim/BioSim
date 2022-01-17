
__author__ = 'Andrine Zimmermann, Karin Mollatt'
__email__ = 'andrine.zimmermann@nmbu.no, karin.mollatt@nmbu.no'

import pytest
from biosim.landscapes import Lowland, Highland, Desert, Water


@pytest.mark.parametrize('class_to_test', [Lowland, Highland, Desert, Water])
class TestLandscapes:
    """
    Class for testing the landscapes superclass.
    """

    # Tests for set_params method
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
        herb_list = [{'species': 'Herbivore',
                      'age': 5,
                      'weight': 20}
                     for _ in range(10)]
        obj.animals_population(herb_list)
        obj.params_fodder['f_max'] = 150
        obj.grow_fodder()
        obj.feeding_herbs()
        assert obj.amount_fodder == 50          # Every herb wants to eat 10. (10x10=100)

    # Test for feeding_carn_with_herbs
    def test_herbs_get_eaten(self, class_to_test, mocker):
        """
        Testing that the eaten herbivores are removed from the list of present herbivores.

        :param class_to_test: Lowland, Highland, Desert and Water subclasses.
        """
        mocker.patch('random.random', return_value=0)
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
        obj.feeding_carn_with_herbs()
        assert len(obj.list_herbivores) < len(obj.list_carnivores)

    # Test for animal_gives_birth
    def test_herbs_get_born(self, class_to_test):
        """
        Testing that the newborn are added to the population in the cell.

        :param class_to_test: Lowland, Highland, Desert and Water subclasses
        """
        obj = class_to_test()
        herb_list = [{'species': 'Herbivore',
                      'age': 5,
                      'weight': 50}
                     for _ in range(10)]
        obj.animals_population(herb_list)
        obj.animal_gives_birth()
        assert len(obj.list_herbivores) > len(herb_list)

    # Test for animal_dies
    def test_herbs_die(self, class_to_test, mocker):
        """
        Testing that the animal is removed from the rest of population if it dies.

        :param class_to_test: Lowland, Highland, Desert and Water subclasses
        """
        mocker.patch('random.random', return_value=0)
        obj = class_to_test()
        herb_list = [{'species': 'Herbivore',
                      'age': 5,
                      'weight': 20}
                     for _ in range(10)]
        obj.animals_population(herb_list)
        for _ in range(10):
            obj.animal_dies()
        assert len(obj.list_herbivores) < len(herb_list)

    def test_carns_die(self, class_to_test, mocker):
        """
        Testing that the animal is removed from the rest of population if it dies.

        :param class_to_test: Lowland, Highland, Desert and Water subclasses
        """
        mocker.patch('random.random', return_value=0)
        obj = class_to_test()
        carn_list = [{'species': 'Carnivore',
                      'age': 5,
                      'weight': 20}
                     for _ in range(10)]
        obj.animals_population(carn_list)
        for _ in range(200):    # Needs to go through enough years for carnivores to die of old age
            obj.animal_dies()
        assert len(obj.list_carnivores) < len(carn_list)

    # Test for distribute_migrated_animals
    def test_distribute_migrated_herbs(self, class_to_test):
        """
        Testing that the animals that migrates, is put to a list.

        :param class_to_test: Lowland, Highland, Desert and Water subclasses
        """
        obj = class_to_test()
        ini_migrated_herbs, _ = obj.distribute_migrated_animals()
        herb_list = [{'species': 'Herbivore',
                      'age': 5,
                      'weight': 20}
                     for _ in range(20)]
        obj.animals_population(herb_list)
        final_migrated_herbs, _ = obj.distribute_migrated_animals()
        assert len(ini_migrated_herbs) < len(final_migrated_herbs)

    def test_distribute_migrated_carns(self, class_to_test):
        """
        Testing that the animals that migrates, is put to a list.

        :param class_to_test: Lowland, Highland, Desert and Water subclasses
        """
        obj = class_to_test()
        _, ini_migrated_carns = obj.distribute_migrated_animals()
        carn_list = [{'species': 'Carnivore',
                      'age': 5,
                      'weight': 20}
                     for _ in range(20)]
        obj.animals_population(carn_list)
        _, final_migrated_carns = obj.distribute_migrated_animals()
        assert len(ini_migrated_carns) < len(final_migrated_carns)

    # Test for annual_restart_migration
    def test_herb_has_migrated_is_false(self, class_to_test):
        """
        Testing that the animal's migration 'flag' is changed to False, if it
        has migrated.

        :param class_to_test: Lowland, Highland, Desert and Water subclasses
        """
        obj = class_to_test()
        herb_list = [{'species': 'Herbivore',
                      'age': 5,
                      'weight': 20}
                     for _ in range(10)]
        obj.animals_population(herb_list)
        for i in range(10):
            migrated_herbs, _ = obj.distribute_migrated_animals()
        obj.annual_restart_migration()
        for herb in migrated_herbs:
            assert herb.has_migrated is False

    def test_carn_has_migrated_is_false(self, class_to_test):
        """
        Testing that the animal's migration 'flag' is changed to False, if it
        has migrated.

        :param class_to_test: Lowland, Highland, Desert and Water subclasses
        """
        obj = class_to_test()
        carn_list = [{'species': 'Carnivore',
                      'age': 5,
                      'weight': 20}
                     for _ in range(10)]
        obj.animals_population(carn_list)
        for i in range(10):
            _, migrated_carns = obj.distribute_migrated_animals()
        obj.annual_restart_migration()
        for carn in migrated_carns:
            assert carn.has_migrated is False

class TestLowland:

    @pytest.fixture
    def standard_lowland(self):
        """
        Fixture setting standard lowland.
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
