
__author__ = 'Andrine Zimmermann, Karin Mollatt'
__email__ = 'andrine.zimmermann@nmbu.no, karin.mollatt@nmbu.no'

"""
Script for testing the complete simulation.

This is heavily inspired by Plesser, H.E. 'sample_sim.py' and 'check_sim.py'.
"""

from biosim.simulation import BioSim
import textwrap

geogr = """\
              WWWWWWWWWWWWWWWWWWWWW
              WHHHHHLLLLWWLLLLLLLWW
              WHHHHHLLLLWWLLLLLLLWW
              WHHHHHLLLLWWLLLLLLLWW
              WWHHLLLLLLLWWLLLLLLLW
              WWHHLLLLLLLWWLLLLLLLW
              WWWWWWWWHWWWWLLLLLLLW
              WHHHHHLLLLWWLLLLLLLWW
              WHHHHHHHHHWWLLLLLLWWW
              WHHHHHDDDDDLLLLLLLWWW
              WHHHHHDDDDDLLLLLLLWWW
              WHHHHHDDDDDLLLLLLLWWW
              WHHHHHDDDDDWWLLLLLWWW
              WHHHHDDDDDDLLLLWWWWWW
              WWHHHHDDDDDDLWWWWWWWW
              WWHHHHDDDDDLLLWWWWWWW
              WHHHHHDDDDDLLLLLLLWWW
              WHHHHDDDDDDLLLLWWWWWW
              WWHHHHDDDDDLLLWWWWWWW
              WWWHHHHLLLLLLLWWWWWWW
              WWWHHHHHHWWWWWWWWWWWW
              WWWWWWWWWWWWWWWWWWWWW"""

geogr = textwrap.dedent(geogr)

ini_herbs = [{'loc': (2, 7),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(200)]}]
ini_carns = [{'loc': (2, 7),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]

sim = BioSim(geogr, ini_herbs + ini_carns, seed=1,
             hist_specs={'fitness': {'max': 1.0, 'delta': 0.05},
                         'age': {'max': 60.0, 'delta': 2},
                         'weight': {'max': 60, 'delta': 2}},
             cmax_animals={'Herbivore': 200, 'Carnivore': 50})
sim.simulate(100)

input('Press ENTER')

