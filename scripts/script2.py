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

ini_herbs = [{'loc': (1, 1),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]
ini_carns = [{'loc': (1, 1),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(20)]}]

# lo = Lowland()
#isl = Island("L", ini_herbs)

params_fodder = {"f_max": 800}

Lowland.set_params(params_fodder)
# lo.animals_population(poph)
# isl.adding_population(ini_carns)

plt.figure(figsize=(8, 6))

for seed in range(100, 120):
    random.seed(seed)

    herb_list = []
    carn_list = []
    isl = Island("L", ini_herbs)

    for i in range(50):
        lo = isl.map[(1, 1)]
        # print(lo.amount_herbs, lo.amount_carns)
        lo.eating_process()
        lo.animal_gives_birth()
        lo.animal_gets_older()
        lo.animal_dies()

        herb_list.append(lo.amount_herbs)
        carn_list.append(lo.amount_carns)

    isl.adding_population(ini_carns)
    for i in range(50, 300):
        lo = isl.map[(1, 1)]
        # print(lo.amount_herbs, lo.amount_carns)
        lo.eating_process()
        lo.animal_gives_birth()
        lo.animal_gets_older()
        lo.animal_dies()

        herb_list.append(lo.amount_herbs)
        carn_list.append(lo.amount_carns)

    print(lo.amount_herbs, lo.amount_carns)

    plt.plot(herb_list, 'b')
    plt.plot(carn_list, 'r')

plt.show()

# print(statistics.mean(testlist))

# plt.rcParams['figure.figsize'] = (12, 5)
# plt.plot([i for i in range(300)], amount)
# plt.legend()

# antall = lo.count_herbs()
# print(antall)
