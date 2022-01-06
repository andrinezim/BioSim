
__author__ = 'Andrine Zimmermann, Karin Mollatt'
__email__ = 'andrine.zimmermann@nmbu.no, karin.mollatt@nmbu.no'

"""
Module for herbivores
"""
from biosim.landscapes import Lowland
from math import exp
import random

class Herbivores:
    """
    Class for herbivores.
    """
    default_params = {
                    "w_birth": 8.0,
                    "sigma_birth": 1.5,
                    "beta": 0.9,
                    "eta": 0.05,
                    "a_half": 40.0,
                    "phi_age": 0.6,
                    "w_half": 10.0,
                    "phi_weight": 0.1,
                    "mu": 0.25,
                    "gamma": 0.2,
                    "zeta": 3.5,
                    "xi": 1.2,
                    "omega": 0.4,
                    "F": 10.0,
                    "DeltaPhiMax": None}

    @classmethod
    def set_params(cls, incoming_params):
        """
        Method for setting parameters.

        :param incoming_params: Dictionary with parameters to replace default parameters.
        """
        for parameter_key in incoming_params:
            if parameter_key not in cls.default_params:
                raise ValueError('Invalid parameter name: ' + parameter_key)
            if incoming_params[parameter_key] <= 0:
                raise ValueError('Parameter value cannot be below zero.')
            if parameter_key == 'DeltaPhiMax' and incoming_params[parameter_key] <= 0:
                raise ValueError('DeltaPhiMax shall be strictly positive.')
            if parameter_key == 'eta' and not 0 <= incoming_params[parameter_key] <= 1:
                raise ValueError('Eta must be in [0,1]')


    def __init__(self, age=0, weight=None):
        """
        Method for saving age and weight values in class

        :param age: Age of animal
        :param weight: Weight of animal
        """
        if age < 0:
            raise ValueError('Age cannot be below zero.')
        else:
            self.age = age

        if weight < 0:
            raise ValueError('Weight cannot be below zero.')
        elif weight is None:
            self.weight = random.gauss(self.default_params['w_birth'], self.default_params['sigma_birth'])
        else:
            self.weight = weight

        # Defining phi value for use in fitness and procreation functions
        self.phi = self.fitness()

    @staticmethod
    def q_func(x, x_half, phi_aw, pos_neg):
        """
        Static function for fitness method

        :param x: current age/weight of animal
        :param x_half: constant parameter for age/weight
        :param phi_aw: constant parameter for age/weight
        :param pos_neg: determines positive(age)/negative(weight)

        :return: value of q function
        """
        q = (1 / (1 + exp(pos_neg * phi_aw * (x - x_half))))

        return q

    def fitness(self):
        """
        Method for calculating fitness of animal.

        :return: Value of phi
        """
        if self.weight <= 0:
            self.phi = 0
        else:
            q_pos = self.q_func(self.age, self.default_params['a_half'], self.default_params['phi_age'], 1)
            q_neg = self.q_func(self.weight, self.default_params['w_half'], self.default_params['phi_weight'], -1)
            self.phi = q_pos * q_neg

        return self.phi

    def aging(self):
        """
        Method for aging each animal. Will be called every new year.
        """
        self.age += 1
        self.weight -= (self.default_params['eta'] * self.weight)
        self.fitness()

    def herbs_eating(self, amount_fodder):
        """
        Method for deciding how much a herbivore eats

        :return: Eaten amount
        """
        if self.default_params['F'] < amount_fodder:
            amount_eaten = self.default_params['F']
        else:
            amount_eaten = amount_fodder

        self.weight += self.default_params['beta']*amount_eaten
        self.fitness()

        return amount_eaten

    def procreation(self):
        amount_herbs = Lowland.count_herbs()
        birth_prob = min(1, self.default_params['gamma']*self.phi*(amount_herbs-1))
        demand = self.default_params['zeta']*(self.default_params['w_birth']+self.default_params['sigma_birth'])

        if amount_herbs < 2:
            return None
        elif self.weight < demand:
            return None
        else:
            if random.random() < birth_prob:
                newborn = type(self)()
                if self.weight > self.default_params['xi'] * newborn.weight:
                    self.weight -= self.default_params['xi'] * newborn.weight
                    return newborn
                else:
                    return None
            else:
                return None

    def death(self):
        """
        Method of deciding if the animal dies or not.

        :return: True if animal dies, and False if it survives.
        """
        random.seed(12345)
        death_prob = self.default_params['omega'] * (1 - self.phi)
        if self.weight == 0:
            return True
        else:
            return random.random() < death_prob

    def __repr__(self):
        string = f'Age: {self.age}, Weight: {self.weight}, Fitness: {self.phi}'
        return string
