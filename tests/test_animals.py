
__author__ = 'Andrine Zimmermann, Karin Mollatt'
__email__ = 'andrine.zimmermann@nmbu.no, karin.mollatt@nmbu.no'

import pytest_mock

"""
Testing the functions in animals.py
"""

from biosim.animals import Herbivores, Carnivores
import pytest


class TestAnimals:

    # Tests for set_param method
    def test_set_params(self, request):
        pass

    @pytest.fixture
    def standard_herb(self):
        """
        Fixture setting standard herbivore.

        :return: Standard herbivore class.
        """
        return Herbivores()

    @pytest.fixture
    def standard_carn(self):
        """
        Fixture setting standard carnivore.

        :return: Standard carnivore class.
        """
        return Carnivores()

    def test_negative_param_value(self, standard_herb):
        """
        Testing that we get a ValueError if the parameters are negative.

        :param standard_herb: Standard herbivore class.
        """
        with pytest.raises(ValueError):
            standard_herb.set_params({"sigma_birth": -1.5})

    def test_deltaphimax_negative(self, standard_carn):
        """
        Testing that if we get the parameter DeltaPhiMax and it's below zero,
        a ValueError will be raised.

        :param standard_carn: Standard carnivore class.
        """
        with pytest.raises(ValueError):
            standard_carn.set_params({"DeltaPhiMax": -1.5})
        with pytest.raises(ValueError):
            standard_carn.set_params({"DeltaPhiMax": 0})

    def test_eta_0_1(self, standard_herb):
        """
        Testing that if we get the parameter eta and it's not in [0,1],
        a ValueError will be raised.

        :param standard_herb: Standard herbivore class.
        """
        with pytest.raises(ValueError):
            standard_herb.set_params({"eta": 2})
        with pytest.raises(ValueError):
            standard_herb.set_params({"eta": -2})

    def test_param_update(self, standard_herb):
        """
        Testing if the default params are updating.

        :param standard_herb: Standard herbivore class.
        """
        current_params = standard_herb.default_params
        new_params = {
            "w_birth": 9.0,
            "sigma_birth": 2.5,
            "beta": 1.9,
            "eta": 0.55}

        new_params = standard_herb.set_params(new_params)
        assert new_params != current_params

    def test_invalid_param_name(self, standard_herb):
        """
        Testing that if we get an invalid parameter name, a KeyError is raised.

        :param standard_herb: Standard herbivore class.
        """
        with pytest.raises(KeyError):
            standard_herb.set_params({"alpha": 1})


    # Tests for __init__ method
    def test_age_negative(self):
        """
        Testing that if we get a negative age, a ValueError will be raised.
        """
        with pytest.raises(ValueError):
            Herbivores(age=-1)

    def test_age_positive(self, standard_herb):
        """
        Testing that if we get a positive age, the class object's age is set to incoming age.

        :param standard_herb: Standard herbivore class.
        """
        standard_herb.age = 3
        assert standard_herb.age == 3

    def test_age_int(self, standard_herb):
        """
        Testing that the age can only be an integer, if not a ValueError will be raised.

        :param standard_herb: Standard herbivore class.
        """
        try:
            standard_herb.age = 3.3
        except ValueError as error:
            print(error)

    def test_weight_none(self, standard_herb):
        """
        Testing if we don't get a weight input, the weight will be drawn from a Gaussian distribution.

        :param standard_herb: Standard herbivore class.
        """
        # Mocker function
        pass

    def test_weight_negative(self):
        """
        Testing that if we get a negative weight, a ValueError will be raised.
        """
        with pytest.raises(ValueError):
            Herbivores(weight=-3)

    def test_weight_positive(self):
        pass

    def test_init_phi(self):
        pass


    # Tests for q_func and fitness methods

    def test_q_func(self):
        pass

    def test_fitness_weight_negative_equal(self):
        pass

    def test_fitness_weight_positive(self):
        pass


    # Tests for aging method
    # mocking?

    def test_aging(self):
        pass

    def test_annual_weight_loss(self):
        pass

    def test_annual_fitness_update(self):
        pass


    # Tests for procreation method

    def test_birth_prob(self):
        pass

    def test_demand(self):
        pass

    def test_weight_lower_than_demand(self):
        pass

    def test_random_lower_than_birth_prob(self):
        pass

    def test_random_higher_than_birth_prob(self):
        pass

    def test_weight_higher_than_newborn(self):
        pass

    def test_weight_lower_than_newborn(self):
        pass


    # Tests for death method

    def test_death_prob(self):
        pass

    def test_weight_zero(self):
        pass

    def test_weight_not_zero(self):
        pass


class TestHerbivores:

    # Tests for herbs_eating method

    def test_F_lower_than_amount_fodder(self):
        pass

    def test_F_higher_equal_than_amount_fodder(self):
        pass

    def test_weight_gain(self):
        pass


class TestCarnivores:

    # Tests for carns_eating_herbs method

    def test_fitness_carn_lower_equal_than_fitness_herb(self):
        pass

    def test_difference_between_0_deltaphimax(self):
        pass

    def test_difference_higher_than_deltaphimax(self):
        pass

    def test_random_lower_equal_prob_kill(self):
        pass

    def test_amount_eaten(self):
        pass

    def test_weight_gain(self):
        pass

    def test_append_herb(self):
        pass

    def test_weight_eaten_herbs_update(self):
        pass

    def test_weight_eaten_herbs_higher_equal_F(self):
        pass


pytest.main(['test_animals.py'])
