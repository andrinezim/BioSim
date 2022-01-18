
__author__ = 'Andrine Zimmermann, Karin Mollatt'
__email__ = 'andrine.zimmermann@nmbu.no, karin.mollatt@nmbu.no'

"""
Script for testing out the herbivores and carnivores are behaving as they should
in one Lowland cell.
"""

from biosim.landscapes import Lowland
from biosim.island import Island

import matplotlib.pyplot as plt
import random
import textwrap

geogr = """\
           WWW
           WLW
           WWW"""
geogr = textwrap.dedent(geogr)

poph = [{'species': 'Herbivore',
            'age': 5,
            'weight': 20}
            for _ in range(50)]

ini_herbs = [{'loc': (2, 2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]
ini_carns = [{'loc': (2, 2),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(20)]}]

params_fodder = {"f_max": 800}

Lowland.set_params(params_fodder)

plt.figure(figsize=(8, 6))

for seed in range(100, 120):
    random.seed(seed)

    herb_list = []
    carn_list = []
    isl = Island(geogr, ini_herbs)

    for i in range(50):
        lo = isl.map[(2, 2)]
        lo.eating_process()
        lo.animal_gives_birth()
        lo.animal_gets_older()
        lo.animal_dies()

        herb_list.append(lo.amount_herbs)
        carn_list.append(lo.amount_carns)

    isl.adding_population(ini_carns)
    for i in range(50, 300):
        lo = isl.map[(2, 2)]
        lo.eating_process()
        lo.animal_gives_birth()
        lo.animal_gets_older()
        lo.animal_dies()

        herb_list.append(lo.amount_herbs)
        carn_list.append(lo.amount_carns)

    print(lo.amount_herbs, lo.amount_carns)

