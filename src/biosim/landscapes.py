
__author__ = 'Andrine Zimmermann, Karin Mollatt'
__email__ = 'andrine.zimmermann@nmbu.no, karin.mollatt@nmbu.no'


"""
Module for Lowland
"""
from biosim.animals import Herbivores

class Lowland:

    params_fodder = {"f_max": 800}

    @classmethod
    def set_params(cls, incoming_params):
        """
        Method for setting parameters.

        :param incoming_f_max: The amount of fodder available for all herbivores in a cell.
        """
        for parameter_key in incoming_params:
            if parameter_key in cls.params_fodder:
                if incoming_params[parameter_key] < 0:
                    raise ValueError('Amount of fodder available cannot be below zero.')
                cls.params_fodder.update(incoming_params)
            else:
                raise ValueError('Invalid parameter name: ' + parameter_key)

    def __init__(self):
        """
        Method for saving values in class.
        """
        # Defining empty list for use in herbs_population function
        self.list_herbivores = []

        # Defining amount of fodder for use in feeding_herbs and feeding_carns functions.
        self.amount_fodder = self.param_f_max

        # Defining amount of fodder for use in count_herbs
        self.amount_herbs = 0

    def herbs_population(self, ini_population):
        """
        Method for distributing herbivores into a list.

        :param ini_population: Initial population in one cell.
        :return: List with herbivores in one cell.
        """
        for pop_dict in ini_population:
            if pop_dict['species'] == 'Herbivore':
                self.list_herbivores.append(Herbivores(pop_dict['age'], pop_dict['weight']))
            else:
                raise TypeError('The only accepted species is herbivore.')
        return self.list_herbivores

    def count_herbs(self):
        """
        Method for counting herbivores.

        :return: Amount of herbivores.
        """
        self.amount_herbs = len(self.list_herbivores)
        return self.amount_herbs

    def feeding_herbs(self):
        """
        Method for adjusting amount of fodder available in the cell.
        """
        self.list_herbivores = sorted(self.list_herbivores, key=lambda f: getattr(f, 'phi'))

        for herb in self.list_herbivores:
            if self.amount_fodder > 0:
                amount_eaten = herb.herbs_eating(self.amount_fodder)
                self.amount_fodder -= amount_eaten

    def animal_gives_birth(self):
        """
        Method for adding a newborn to the population in the cell.
        """
        for herb in self.list_herbivores:
            newborn = herb.procreation(self.amount_herbs)
            if newborn is not None:
                self.list_herbivores.append(newborn)

    def animal_dies(self):
        """
        Method for removing dead animals from the rest of the population.
        """
        self.list_herbivores = [herb for herb in self.list_herbivores if not Herbivores.death()]

    def animal_gets_older(self):
        """
        Method for aging an animal.
        """
        for herb in self.list_herbivores:
            herb.aging()
