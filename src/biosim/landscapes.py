
__author__ = 'Andrine Zimmermann, Karin Mollatt'
__email__ = 'andrine.zimmermann@nmbu.no, karin.mollatt@nmbu.no'


"""
Module for Landscapes 
"""
from .animals import Herbivores, Carnivores

import random


class Landscapes:
    """
    Class for Landscapes with subclasses Lowland, Highland, Desert and Water.
    """

    params_fodder = None

    @classmethod
    def set_params(cls, incoming_params):
        """
        Method for setting parameters.

        :param incoming_params: The amount of fodder available for all animals in a cell.
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
        # Defining empty lists for use in animals_population function
        self.list_herbivores = []
        self.list_carnivores = []

        # Defining amount of fodder for use in feeding_herbs and feeding_carns functions.
        self.amount_fodder = 0

    def animals_population(self, ini_population):
        """
        Method for distributing herbivores into a list.

        :param ini_population: Initial population in one cell.
        :return: List with herbivores in one cell.
        """
        for pop_dict in ini_population:
            if pop_dict["species"] == "Herbivore":
                self.list_herbivores.append(Herbivores(pop_dict["age"], pop_dict["weight"]))
            elif pop_dict["species"] == "Carnivore":
                self.list_carnivores.append(Carnivores(pop_dict["age"], pop_dict["weight"]))
            else:
                raise TypeError('The only accepted species is herbivore.')

    def eating_process(self):
        """
        Method for the eating process.

        Begins with regrowing every year and making fodder available depending on the landscape type.
        Then the herbivores eat in descending order of fitness.
        """
        self.grow_fodder()
        self.feeding_herbs()
        self.feeding_carn_with_herbs()

    def grow_fodder(self):
        """
        Method for making fodder available.

        This function will be overwritten by subclasses.
        """
        pass

    def feeding_herbs(self):
        """
        Method for adjusting amount of fodder available in the cell.
        """
        self.list_herbivores = sorted(self.list_herbivores, key=lambda f: getattr(f, 'phi'), reverse=True)

        for herb in self.list_herbivores:
            if self.amount_fodder > 0:
                amount_eaten = herb.herbs_eating(self.amount_fodder)
                self.amount_fodder -= amount_eaten

    def feeding_carn_with_herbs(self):
        """
        Method for feeding carnivore with herbivores.

        :return:
        """
        self.list_herbivores = sorted(self.list_herbivores, key=lambda f: getattr(f, 'phi'))
        random.shuffle(self.list_carnivores)

        for carn in self.list_carnivores:
            if len(self.list_herbivores) > 0:
                eaten_herbs = carn.carns_eating_herbs(self.list_herbivores)
                if eaten_herbs is not None:
                    self.list_herbivores = [herb for herb in self.list_herbivores
                                            if herb not in eaten_herbs]

    def animal_gives_birth(self):
        """
        Method for adding a newborn to the population in the cell.
        """
        newborn_herbs = []
        newborn_carns = []

        for herb in self.list_herbivores:
            newborn = herb.procreation(len(self.list_herbivores))
            if newborn is not None:
                newborn_herbs.append(newborn)
        self.list_herbivores.extend(newborn_herbs)

        for carn in self.list_carnivores:
            newborn = carn.procreation(len(self.list_carnivores))
            if newborn is not None:
                newborn_carns.append(newborn)
        self.list_carnivores.extend(newborn_carns)

    def animal_dies(self):
        """
        Method for removing dead animals from the rest of the population.
        """
        self.list_herbivores = [herb for herb in self.list_herbivores if not herb.death()]

        self.list_carnivores = [carn for carn in self.list_carnivores if not carn.death()]

    def animal_gets_older(self):
        """
        Method for aging an animal.
        """
        for herb in self.list_herbivores:
            herb.aging()

        for carn in self.list_carnivores:
            carn.aging()

    @property
    def amount_herbs(self):
        return len(self.list_herbivores)

    @property
    def amount_carns(self):
        return len(self.list_carnivores)


class Lowland(Landscapes):
    """
    Subclass Lowland with superclass Landscapes.
    """
    params_fodder = {"f_max": 800}

    def __init__(self):
        """
        Method for saving values in class.
        """
        super().__init__()

    def grow_fodder(self):
        """
        Method for making fodder available.
        """
        self.amount_fodder = self.params_fodder["f_max"]


class Highland(Landscapes):
    """
    Subclass Highland with superclass Landscapes.
    """
    params_fodder = {"f_max": 300}

    def __init__(self):
        """
        Method for saving values in class.
        """
        super().__init__()

    def grow_fodder(self):
        """
        Method for making fodder available.
        """
        self.amount_fodder = self.params_fodder["f_max"]


class Desert(Landscapes):
    """
    Subclass Desert with superclass Landscapes.
    """
    params_fodder = {"f_max": 0}

    def __init__(self):
        """
        Method for making fodder available.
        """
        super().__init__()

    def grow_fodder(self):
        """
        Method for making fodder available.
        """
        self.amount_fodder = self.params_fodder["f_max"]


class Water(Landscapes):
    """
    Subclass Water with superclass Landscapes.
    """
    params_fodder = {"f_max": 0}

    def __init__(self):
        """
        Method for making fodder available.
        """
        super().__init__()

    def grow_fodder(self):
        """
        Method for making fodder available.
        """
        self.amount_fodder = self.params_fodder["f_max"]
