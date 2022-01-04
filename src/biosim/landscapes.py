"""
Module for Lowland
"""
from .animals import Herbivores

class Lowland:

    def __init__(self, f_max=800):
        self.amount_fodder = f_max

    def feeding_herbs(self, F=10):
        if F < self.amount_fodder:
            amount_eaten = F
        else:
            amount_eaten = self.amount_fodder

        self.amount_fodder -= amount_eaten
        Herbivores.weight_change()
        Herbivores.fitness()

        return amount_eaten