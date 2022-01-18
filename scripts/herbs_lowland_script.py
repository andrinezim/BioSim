
__author__ = 'Andrine Zimmermann, Karin Mollatt'
__email__ = 'andrine.zimmermann@nmbu.no, karin.mollatt@nmbu.no'

"""
Script for herbivores and lowland.
"""

from biosim.animals import Herbivores
from biosim.landscapes import Lowland
from biosim.island import Island
from biosim.simulation import BioSim
import textwrap

poph = [{'species': 'Herbivore',
            'age': 5,
            'weight': 20}
            for _ in range(5)]

c = Lowland()
list_h = c.animals_population(ini_population=poph)
print(list_h)

#-----------------

poph = [{'species': 'Herbivore',
                 'age': 5,
                 'weight': 20} for _ in range(50)
                 ]

list_aw = [[8,0], [8,1], [8,20], [8,20]]
for age, weight in list_aw:
    Herbivores(age, weight).fitness()
    print(Herbivores(age, weight).death())

#---------------------

geogr = """\
           WWW
           WLW
           WWW"""
geogr = textwrap.dedent(geogr)

#------------------------
print('--------------')
test_params = {
                    "w_birth": 10.0,
                    "sigma_birth": 2.5}
test_list = ['Herbivore' for _ in range(2)]
#b = BioSim(island_map=geogr, ini_pop=poph, seed=123)
#for animal in test_list:
#    print(b.set_animal_parameters(animal, test_params))
#----------------------------
