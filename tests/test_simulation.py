
__author__ = 'Andrine Zimmermann, Karin Mollatt'
__email__ = 'andrine.zimmermann@nmbu.no, karin.mollatt@nmbu.no'

import pytest

from biosim.simulation import BioSim


class TestSimulation:

    @pytest.fixture(autouse=True)
    def standard_simulation(self):
        """
        Fixture setting standard simulation.
        """
        ini_pop = [{'loc': (3, 3),
                    'pop': [{'species': 'Herbivore',
                             'age': 5,
                             'weight': 20}
                            for _ in range(20)]},
                   {'loc': (3, 3),
                    'pop': [{'species': 'Carnivore',
                             'age': 5,
                             'weight': 20}
                            for _ in range(10)]}]
        self.standard_simulation = BioSim(ini_pop=ini_pop, island_map="WWWWW\nWWLWW\nWLLLW\nWWLWW\nWWWWW",
                                          seed=1)

    # Test to simulate function
    def test_value_error_vis_years(self):
        """
        Testing that we get a ValueError if img_years is not a multiple of vis_years.
        """
        # obj = BioSim(ini_pop=[], island_map="WWWWW\nWWLWW\nWLLLW\nWWLWW\nWWWWW",
                     # seed=1, img_years=5, vis_years=2)
        self.standard_simulation.img_years = 5
        self.standard_simulation.vis_years = 2
        with pytest.raises(ValueError):
            self.standard_simulation.simulate(10)

    def test_current_year_increase(self):
        """
        Testing that the current year increases every year.
        """
        self.standard_simulation.simulate(10)
        assert self.standard_simulation._current_year == 10

    def test_get_year(self):
        """
        Testing if the simulation returns the correct year.
        """
        self.standard_simulation.simulate(num_years=3)
        assert self.standard_simulation.year == 3
        self.standard_simulation.simulate(num_years=4)
        assert self.standard_simulation.year == 7

    def test_get_num_animals(self):
        """
        Testing that the simulation returns the correct number of animals.
        """
        obj = BioSim(ini_pop=[], island_map="WWWWW\nWWLWW\nWLLLW\nWWLWW\nWWWWW",
                     seed=1, img_years=5, vis_years=2)
        assert obj.num_animals == 0

    def test_get_animal_per_species(self):
        """
        Testing that the simulation returns the correct amount of animals per species.
        """
        obj = BioSim(ini_pop=[], island_map="WWWWW\nWWLWW\nWLLLW\nWWLWW\nWWWWW",
                     seed=1, img_years=5, vis_years=2)
        assert obj.num_animals_per_species == {'Herbivore': 0, 'Carnivore': 0}


pytest.main(['test_simulation.py'])
