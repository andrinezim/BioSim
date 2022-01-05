"""
Module for herbivores
"""
#from .landscapes import Lowland
from math import exp

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


    def __init__(self, age, weight):
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
        else:
            self.weight = weight

        # Defining phi value for use in fitness and procreation functions
        self.phi = 0

    @staticmethod
    def q(x, x_half, phi_aw, pos_neg):
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
        if self.weight == 0:
            self.phi = 0
        else:
            q_pos = self.q(self.age, self.default_params['a_half'], self.default_params['phi_age'], 1)
            q_neg = self.q(self.weight, self.default_params['w_half'], self.default_params['phi_weight'], -1)
            self.phi = q_pos * q_neg

        return self.phi

    def aging(self):
        """
        Method for aging each animal. Will be called every new year.
        """
        self.age += 1
        self.weight = self.weight - (self.default_params['eta'] * self.weight)
        self.fitness()

    def herbs_eating(self):
        """
        Method for deciding how much a herbivore eats

        :return: Eaten amount
        """
        amount_fodder = Lowland.feeding_herbs()
        if self.default_params['F'] < amount_fodder:
            amount_eaten = self.default_params['F']
        else:
            amount_eaten = amount_fodder

        self.weight += self.default_params['beta']*amount_eaten
        self.fitness()

        return amount_eaten

    def procreation(self):
        pass

    def death(self):
        pass

    def __repr__(self):
        string = f'Age: {self.age}, Weight: {self.weight}, Fitness: {self.phi}'
        return string

if __name__ == "__main__":
    poph = [{'species': 'Herbivore',
                 'age': 5,
                 'weight': 20} for _ in range(50)
                 ]

    list_aw = [[8,20], [8,20], [8,20], [8,20]]
    for age, weight in list_aw:
        print(Herbivores(age, weight).__repr__())
        Herbivores(age, weight).aging()
        print(Herbivores(age, weight).__repr__())

