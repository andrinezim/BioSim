"""
Module for herbivores
"""
import math

class Herbivores:

    def __init__(self, age, weight, f_max=800):
        self.age = age
        self.weight = weight
        self.f_max = f_max


    def aging(self):
        self.age += 1

    def fitness(self, a_half=40, phi_age=0.6, w_half=10, phi_weight=0.1):
        if self.weight == 0:
            phi = 0
        else:
            phi = (1/(1+math.exp(phi_age*(self.age-a_half)))) * (1/(1+math.exp(-phi_weight*(self.weight-w_half))))
        return phi

    def feeding(self, F):
        pass

    def weight_change(self, beta, eta):
        self.weight -= eta*self.weight
        pass

    def procreation(self):
        pass

    def migration(self):
        pass

    def death(self):
        pass
