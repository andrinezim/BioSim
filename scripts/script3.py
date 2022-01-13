
from biosim.island import Island
from biosim.simulation import BioSim
import textwrap

geogr = """\
        WWWWW
        WWLWW
        WLLLW
        WWLWW
        WWWWW"""

geogr = textwrap.dedent(geogr)

ini_herbs = [{'loc': (3, 3),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(100)]}]

sim = BioSim(island_map=geogr, ini_pop=ini_herbs, seed=123456, vis_years=1)
sim.set_animal_parameters('Herbivore', {'mu': 1, 'omega': 0.00001, 'gamma': 0.00001, 'a_half': 1000})
sim.simulate(1)

for cell in sim.island.map:
    print(cell, len(sim.island.map[cell].list_herbivores))

