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
        pass

