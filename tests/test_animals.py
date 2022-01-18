
__author__ = 'Andrine Zimmermann, Karin Mollatt'
__email__ = 'andrine.zimmermann@nmbu.no, karin.mollatt@nmbu.no'

"""
Testing the functions in animals.py
"""

from biosim.animals import Herbivores, Carnivores
import pytest
from math import exp


class TestAnimals:

    # Tests for set_param method
    @pytest.fixture(autouse=True)
    def standard_herb(self):
        """
        Fixture setting standard herbivore.

        :return: Standard herbivore class.
        """
        self.herb = Herbivores()

    @pytest.fixture(autouse=True)
    def standard_carn(self):
        """
        Fixture setting standard carnivore.

        :return: Standard carnivore class.
        """
        self.carn = Carnivores()

    def test_negative_param_value(self):
        """
        Testing that we get a ValueError if the parameters are negative.
        """
        with pytest.raises(ValueError):
            self.herb.set_params({"sigma_birth": -1.5})

    def test_deltaphimax_negative(self):
        """
        Testing that if we get the parameter DeltaPhiMax and it's below zero,
        a ValueError will be raised.
        """
        with pytest.raises(ValueError):
            self.carn.set_params({"DeltaPhiMax": -1.5})
        with pytest.raises(ValueError):
            self.carn.set_params({"DeltaPhiMax": 0})

    def test_eta_0_1(self):
        """
        Testing that if we get the parameter eta and it's not in [0,1],
        a ValueError will be raised.
        """
        with pytest.raises(ValueError):
            self.herb.set_params({"eta": 2})
        with pytest.raises(ValueError):
            self.herb.set_params({"eta": -2})

    def test_param_update(self):
        """
        Testing if the default params are updating.
        """
        current_params = self.herb.default_params
        new_params = {
            "w_birth": 9.0,
            "sigma_birth": 2.5,
            "beta": 1.9,
            "eta": 0.55}

        new_params = self.herb.set_params(new_params)
        assert new_params != current_params

    def test_invalid_param_name(self):
        """
        Testing that if we get an invalid parameter name, a KeyError is raised.
        """
        with pytest.raises(KeyError):
            self.herb.set_params({"alpha": 1})

    # Tests for __init__ method
    def test_age_negative(self):
        """
        Testing that if we get a negative age, a ValueError will be raised.
        """
        with pytest.raises(ValueError):
            Herbivores(age=-1)

    def test_age_positive(self):
        """
        Testing that if we get a positive age, the class object's age is set to incoming age.
        """
        self.herb.age = 3
        assert self.herb.age == 3

    def test_age_int(self):
        """
        Testing that the age can only be an integer, if not a ValueError will be raised.
        """
        with pytest.raises(ValueError):
            Herbivores(age=3.3)

    def test_weight_none(self, mocker):
        """
        Testing if we don't get a weight input, the weight will be drawn from a Gaussian distribution.

        Using the mocker function to trick the function random.gauss to return 1.
        """
        mocker.patch("random.gauss", return_value=1)
        assert Herbivores().weight == 1

    def test_weight_negative(self):
        """
        Testing that if get a negative weight, a ValueError will be raised.
        """
        with pytest.raises(ValueError):
            Herbivores(weight=-3)

    def test_weight_positive(self):
        """
        Testing that if the weight is positive, it is set to the weight input.
        """
        self.herb.weight = 5
        assert self.herb.weight == 5

    # Tests for q_func and fitness methods
    @pytest.mark.parametrize("x, x_half, phi_aw, pos_neg, expected",
                             [[5, 5, 0.5, 1, 0.5],
                              [6, 4, 1, -1, (1/(1+(1/exp(2))))]])
    def test_q_func(self, x, x_half, phi_aw, pos_neg, expected):
        """
        Testing if the q function calculates the correct value.

        Using the pytest.mark.parametrize to run through the test multiple times,
        without needing duplicated code.

        The expected values are precalculated by hand.
        """
        q = self.herb.q_func(x, x_half, phi_aw, pos_neg)

        assert q == expected

    def test_fitness_weight_negative_equal(self):
        """
        Testing that if the weight is zero or below, the fitness is zero.
        """
        assert Herbivores(weight=0).phi == 0

    def test_fitness_weight_positive(self):
        """
        Testing if we get a positive weight, the weight is set to this.
        """
        self.herb.weight = 3
        assert self.herb.weight == 3

    # Tests for aging method
    def test_aging(self):
        """
        Testing if the animals ages every time the function is called.
        """
        self.herb.age = 3
        self.herb.aging()
        assert self.herb.age == 4

    def test_annual_weight_loss(self):
        """
        Testing if the animals lose weight every year.
        """
        current_weight = self.herb.weight
        self.herb.aging()
        assert self.herb.weight == (current_weight - self.herb.default_params["eta"] * current_weight)

    def test_annual_fitness_update(self):
        """
        Testing that the weight updates when calling on the fitness function.
        """
        current_phi = self.herb.phi
        self.herb.weight = 7
        self.herb.fitness()
        assert self.herb.phi != current_phi

    # Tests for procreation method
    def test_weight_lower_than_demand(self):
        """
        Testing if the function returns None if the weight of the animal
        is lower than our demand.
        Setting the weight to be low, to ensure that we are lower than the demand.
        """
        demand = self.herb.default_params['zeta'] * \
                 (self.herb.default_params['w_birth']+self.herb.default_params['sigma_birth'])
        self.herb.weight = demand - 10
        assert self.herb.procreation(10) is None

    def test_random_higher_than_birth_prob(self, mocker):
        """
        Testing that if the random.random() function gives a number that is higher than
        birth_prob = min(1, self.herb.default_params['gamma']*self.herb.phi*(amount_same_species-1)),
        the procreation() method will return None

        Using mocker to trick the function random.random to return 20, which we can see is above
        the birth probability.
        """
        amount_same_species = 10
        mocker.patch("random.random", return_value=20)
        assert self.herb.procreation(amount_same_species) is None

    def test_weight_higher_than_newborn(self):
        """
        Testing that the animal's weight decreases, after giving birth, if their weight
        is higher than the newborns weight (drawn from a gaussian distribution) times the
        parameter "xi".
        """
        self.herb.weight = 50
        ini_weight = self.herb.weight
        baby = self.herb.procreation(10)
        assert self.herb.weight == ini_weight - (self.herb.default_params["xi"] * baby.weight)

    def test_weight_lower_than_newborn(self):
        """
        Testing that the procreation() method returns None, if the animal's weight is lower
        than the newborn's weight.
        """
        newborn = Herbivores(age=0)
        self.herb.weight = (self.herb.default_params["xi"] * newborn.weight) - 1
        assert self.herb.procreation(10) is None

    # Tests for death method
    def test_death_weight_zero(self):
        """
        Testing that the death() method returns True, if the animal's weight is zero.
        """
        self.herb.weight = 0
        assert self.herb.death() is True

    def test_death_weight_not_zero_lower_than_prob(self, mocker):
        """
        Testing that if the weight is higher than zero AND the drawn number is LOWER
        than the death probability, the death() method returns False.

        Using mocker to trick the random.random function to return the value 0.
        """
        mocker.patch('random.random', return_value=0)
        self.herb.weight = 1
        assert self.herb.death() is True

    def test_death_weight_not_zero_higher_than_prob(self, mocker):
        """
        Testing that if the weight is higher than zero AND the drawn number is HIGHER
        than the death probability, the death() method returns False.

        Using mocker to trick the random.random function to return the value 1.
        """
        mocker.patch('random.random', return_value=1)
        self.herb.weight = 20
        assert self.herb.death() is False

    def test_lower_prob_migrate(self, mocker):
        """
        Testing that if the drawn number is lower than the probability to migrate, that
        the method will return True.

        Using mocker to trick the random.random function to return the value 0.
        """
        mocker.patch('random.random', return_value=0)
        self.herb.phi = 1
        assert self.herb.probability_migrate() is True

    def test_higher_prob_migrate(self, mocker):
        """
        Testing that if the drawn number is higher than the probability to migrate, that
        the method will return False.

        Using mocker to trick the random.random function to return the value 1.
        """
        mocker.patch('random.random', return_value=1)
        self.herb.phi = 0.1
        assert self.herb.probability_migrate() is False

    def test_equal_prob_migrate(self, mocker):
        """
        Testing that if the drawn number is equal to the probability to migrate, that
        the method will return False.

        Using mocker to trick the random.random function to return the value of probability
        to migrate.
        """
        self.herb.phi = 1
        prob_migrate = self.herb.default_params['mu'] * self.herb.phi
        mocker.patch('random.random', return_value=prob_migrate)
        assert self.herb.probability_migrate() is False


class TestHerbivores:

    @pytest.fixture(autouse=True)
    def standard_herb(self):
        """
        Fixture setting standard herbivore.

        :return: Standard herbivore class.
        """
        self.herb = Herbivores()

    # Tests for herbs_eating method
    def test_F_lower_than_amount_fodder(self):
        """
        Testing that if F is lower than the amount of fodder available, the herbivore
        gains the correct amount of weight.

        F is the amount of fodder the herbivore wants to eat.
        """
        ini_weight = self.herb.weight
        self.herb.herbs_eating(20)
        amount_eaten = self.herb.default_params["F"]
        assert self.herb.weight == ini_weight + (self.herb.default_params["beta"] * amount_eaten)

    def test_F_higher_equal_than_amount_fodder(self):
        """
        Testing that if F is higher or equal to the amount of fodder available, the herbivore
        gains the correct amount of weight.

        F is the amount of fodder the herbivore wants to eat.
        """
        ini_weight = self.herb.weight
        self.herb.herbs_eating(5)
        amount_eaten = 5
        assert self.herb.weight == ini_weight + (self.herb.default_params["beta"] * amount_eaten)


class TestCarnivores:

    @pytest.fixture(autouse=True)
    def standard_carn(self):
        """
        Fixture setting standard carnivore.

        :return: Standard carnivore class.
        """
        self.carn = Carnivores()

    # Tests for carns_eating_herbs method
    def test_random_lower_prob_kill(self, mocker):
        """
        Testing that if the drawn number is lower than the killing probability, the weight
        of the animal increases with the correct amount.

        Using mocker to trick the random.random function to return the value of probability
        to migrate.
        """

        mocker.patch('random.random', return_value=0)
        ini_weight = self.carn.weight
        herblist =[Herbivores(age=1, weight=5)]
        self.carn.carns_eating_herbs(herblist)
        amount_eaten = herblist[0].weight
        assert self.carn.weight == ini_weight + self.carn.default_params['beta']*amount_eaten


pytest.main(['test_animals.py'])
