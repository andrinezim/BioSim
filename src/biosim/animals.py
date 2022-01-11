
__author__ = 'Andrine Zimmermann, Karin Mollatt'
__email__ = 'andrine.zimmermann@nmbu.no, karin.mollatt@nmbu.no'

"""
Module for Animals
"""

from math import exp
import random


class Animals:
    """
    Class for animals with subclasses Herbivores and Carnivores.
    """
    default_params = None

    @classmethod
    def set_params(cls, incoming_params):
        """
        Method for setting parameters.

        :param incoming_params: Dictionary with parameters to replace default parameters.
        """
        for parameter_key in incoming_params:
            if parameter_key in cls.default_params:
                if incoming_params[parameter_key] <= 0:
                    raise ValueError('Parameter value cannot be zero or below.')
                if parameter_key == 'DeltaPhiMax' and incoming_params[parameter_key] <= 0:
                    raise ValueError('DeltaPhiMax shall be strictly positive.')
                if parameter_key == 'eta' and not 0 <= incoming_params[parameter_key] <= 1:
                    raise ValueError('Eta must be in [0,1]')
                cls.default_params.update(incoming_params)
            else:
                raise KeyError('Invalid parameter name: ' + parameter_key)

    def __init__(self, age=0, weight=None):
        """
        Method for saving values in class.

        :param age: Age of animal
        :param weight: Weight of animal
        """
        if age < 0:
            raise ValueError('Age cannot be below zero.')
        else:
            self.age = age

        if weight is None:
            self.weight = random.gauss(self.default_params['w_birth'], self.default_params['sigma_birth'])
        elif weight < 0:
            raise ValueError('Weight cannot be below zero.')
        else:
            self.weight = weight

        # Defining phi value for use in fitness and procreation functions
        self.phi = self.fitness()

    @staticmethod
    def q_func(x, x_half, phi_aw, pos_neg):
        """
        Static function for fitness method.

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
        Method for aging each animal. Will increase by one every new year.
        """
        self.age += 1
        self.weight -= (self.default_params['eta'] * self.weight)
        self.fitness()

    def procreation(self, amount_same_species):
        """
        Method to determine the probability of birth.

        Animals can mate if there are at least to animals of the same
        species in one cell. At birth, the mother looses the actual weight of the baby.

        :return: Returns None if there is no birth, and returns newborn if there is new offspring
        """
        birth_prob = min(1, self.default_params['gamma']*self.phi*(amount_same_species-1))
        demand = self.default_params['zeta']*(self.default_params['w_birth']+self.default_params['sigma_birth'])

        if self.weight < demand:
            return None
        else:
            if random.random() < birth_prob:
                newborn = type(self)()
                if self.weight > self.default_params['xi'] * newborn.weight:
                    self.weight -= self.default_params['xi'] * newborn.weight
                    self.fitness()
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
        death_prob = self.default_params['omega'] * (1 - self.phi)
        if self.weight == 0:
            return True
        else:
            return random.random() < death_prob


class Herbivores(Animals):
    """
    Subclass for herbivores, with Animals as superclass.
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
                    "F": 10.0}

    def __init__(self, age=0, weight=None):
        """
        Method for saving values in class.

        :param age: Age of herbivore
        :param weight: Weight of herbivore
        """
        super().__init__(age, weight)

    def herbs_eating(self, amount_fodder):
        """
        Method for deciding how much a herbivore eats.

        :return: Eaten amount
        """
        if self.default_params['F'] < amount_fodder:
            amount_eaten = self.default_params['F']
        else:
            amount_eaten = amount_fodder

        self.weight += self.default_params['beta']*amount_eaten
        self.fitness()

        return amount_eaten


class Carnivores(Animals):
    """
    Subclass for carnivores, with Animals as superclass.
    """
    default_params = {
                    "w_birth": 6.0,
                    "sigma_birth": 1.0,
                    "beta": 0.75,
                    "eta": 0.125,
                    "a_half": 40.0,
                    "phi_age": 0.3,
                    "w_half": 4.0,
                    "phi_weight": 0.4,
                    "mu": 0.4,
                    "gamma": 0.8,
                    "zeta": 3.5,
                    "xi": 1.1,
                    "omega": 0.8,
                    "F": 50.0,
                    "DeltaPhiMax": 10.0}

    def __init__(self, age=0, weight=None):
        """
        Method for saving values in class.
        :param age: Age of carnivore
        :param weight: Weight of carnivore.
        """
        super().__init__(age, weight)

    def carns_eating_herbs(self, sorted_list_fitness_herbs):
        """
        Method for carnivores hunting herbivores.

        One carnivore hunts at a time, in random order. Two carnivores cannot prey on the same
        herbivore. When hunting, each carnivore tries to kill one herbivore at a time, beginning with
        the herbivore with the lowest fitness.

        A carnivore continues to kill herbivores until:
        - the carnivore has eaten an amount F
            - if the herbivore weights more than F, the carnivore only eats amount F
                - the rest of the herbivore goes to waste, and cannot be eaten by another carnivore.
        - or has tried to kill each herbivore in the cell.

        :return: List of dead herbivores.
        """

        eaten_herbs = []
        weight_eaten_herbs = 0

        for herb in sorted_list_fitness_herbs:
            if self.phi <= herb.phi:
                prob_kill = 0
            elif 0 < (self.phi - herb.phi) < self.default_params["DeltaPhiMax"]:
                prob_kill = (self.phi - herb.phi) / self.default_params["DeltaPhiMax"]
            else:
                prob_kill = 1

            if random.random() <= prob_kill:
                amount_eaten = min(herb.weight, self.default_params["F"] - weight_eaten_herbs)
                self.weight += self.default_params["beta"] * amount_eaten
                self.fitness()
                eaten_herbs.append(herb)
                weight_eaten_herbs += amount_eaten

                if weight_eaten_herbs >= self.default_params["F"]:
                    return eaten_herbs

        return eaten_herbs
