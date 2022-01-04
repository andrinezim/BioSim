"""
Module for herbivores
"""
from .landscapes import Lowland
import math

class Herbivores:

    def __init__(self, age, weight):
        self.age = age
        self.weight = weight

    def aging(self):
        self.age += 1

    def fitness(self, a_half=40, phi_age=0.6, w_half=10, phi_weight=0.1):
        if self.weight == 0:
            phi = 0
        else:
            phi = (1/(1+math.exp(phi_age*(self.age-a_half)))) * (1/(1+math.exp(-phi_weight*(self.weight-w_half))))
        return phi

    def weight_change(self, beta=0.9, eta=0.05):
        amount_eaten = Lowland.feeding_herbs()
        self.weight += beta*amount_eaten
        self.weight -= eta*self.weight

    def procreation(self):
        pass

    def death(self):
        pass
