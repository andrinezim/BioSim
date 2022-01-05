"""
Module for Lowland
"""
from .animals import Herbivores

class Lowland:

    param_f_max = 800

    @classmethod
    def set_params(cls, incoming_f_max):
        """
        Method for setting parameters.

        :param incoming_f_max: The amount of fodder available for all herbivores in a cell.
        """
        if incoming_f_max < 0:
            raise ValueError('Amount of fodder available cannot be below zero.')
        else:
            cls.param_f_max = incoming_f_max

    def __init__(self):
        """
        Method for saving values in class.
        """

        # Defining amount of fodder for use in feeding_herbs and feeding_carns functions.
        self.amount_fodder = self.param_f_max

    def feeding_herbs(self):
        if self.amount_fodder > 0:
            amount_eaten = Herbivores.herbs_eating(self.amount_fodder)
            self.amount_fodder -= amount_eaten

