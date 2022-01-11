
__author__ = 'Andrine Zimmermann, Karin Mollatt'
__email__ = 'andrine.zimmermann@nmbu.no, karin.mollatt@nmbu.no'

"""
Testing the functions in animals.py
"""

import pytest

class TestAnimals:

    # Tests for set_param method
    def test_set_params():
        pass

    def test_negative_param_value():
        pass

    def test_deltaphimax_negative():
        pass

    def test_eta_0_1():
        pass

    def test_param_update():
        pass

    def test_invalid_param():
        pass


    # Tests for __init__ method
    def test_age_negative():
        pass

    def test_age_positve():
        pass

    def test_weight_none():
        pass

    def test_weight_negative():
        pass

    def test_weight_positive():
        pass

    def test_init_phi():
        pass


    # Tests for q_func and fitness methods
    def test_q_func():
        pass

    def test_fitness_weight_negative_equal():
        pass

    def test_fitness_weight_positive():
        pass


    # Tests for aging method
    # mocking?
    def test_aging():
        pass

    def test_annual_weight_loss():
        pass

    def test_annual_fitness_update():
        pass


    # Tests for procreation method
    def test_birth_prob():
        pass

    def test_demand():
        pass

    def test_weight_lower_than_demand():
        pass

    def test_random_lower_than_birth_prob():
        pass

    def test_random_higher_than_birth_prob():
        pass

    def test_weight_higher_than_newborn():
        pass

    def test_weight_lower_than_newborn():
        pass


    # Tests for death method
    def test_death_prob():
        pass

    def test_weight_zero():
        pass

    def test_weight_not_zero():
        pass


class TestHerbivores:

    # Tests for herbs_eating method
    def test_F_lower_than_amount_fodder():
        pass

    def test_F_higher_equal_than_amount_fodder():
        pass

    def test_weight_gain():
        pass


class TestCarnivores:

    # Tests for carns_eating_herbs method
    def test_fitness_carn_lower_equal_than_fitness_herb():
        pass

    def test_difference_between_0_deltaphimax():
        pass

    def test_difference_higher_than_deltaphimax():
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





