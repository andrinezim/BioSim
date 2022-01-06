
__author__ = 'Andrine Zimmermann, Karin Mollatt'
__email__ = 'andrine.zimmermann@nmbu.no, karin.mollatt@nmbu.no'

"""
Script for herbivores and lowland.
"""

from biosim.animals import Herbivores
from biosim.landscapes import Lowland

poph = [{'species': 'Herbivore',
            'age': 5,
            'weight': 20}
            for _ in range(5)]

c = Lowland()
list_h = c.herbs_population(ini_population=poph)
print(list_h)

poph = [{'species': 'Herbivore',
                 'age': 5,
                 'weight': 20} for _ in range(50)
                 ]

list_aw = [[8,0], [8,1], [8,20], [8,20]]
for age, weight in list_aw:
    Herbivores(age, weight).fitness()
    print(Herbivores(age, weight).death())