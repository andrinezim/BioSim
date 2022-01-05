"""
Module for herbivores
"""
from .landscapes import Lowland
from math import exp

class Herbivores:

    def __init__(self, age, weight):
        self.age = age
        self.weight = weight

    def aging(self):
        """
        Method for aging each animal. Will be called every new year.
        """
        self.age += 1

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

    def fitness(self, a_half=40, phi_age=0.6, w_half=10, phi_weight=0.1):
        if self.weight == 0:
            phi = 0
        else:
            q_pos = self.q(self.age, a_half, phi_age, 1)
            q_neg = self.q(self.weight, w_half, phi_weight, -1)
            phi = q_pos * q_neg
        return phi

    def weight_change(self, beta=0.9, eta=0.05):
        amount_eaten = Lowland.feeding_herbs()
        self.weight += beta*amount_eaten
        self.weight -= eta*self.weight

    def procreation(self):
        pass

    def death(self):
        pass
