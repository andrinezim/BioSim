
__author__ = 'Andrine Zimmermann, Karin Mollatt'
__email__ = 'andrine.zimmermann@nmbu.no, karin.mollatt@nmbu.no'

"""
Template for BioSim class.
"""

# The material in this file is licensed under the BSD 3-clause license
# https://opensource.org/licenses/BSD-3-Clause
# (C) Copyright 2021 Hans Ekkehard Plesser / NMBU

from .animals import Herbivores, Carnivores
from .landscapes import Lowland, Highland, Desert, Water
from .island import Island
import random
import os


class BioSim:
    def __init__(self,
                 island_map,
                 ini_pop,
                 seed,
                 vis_years=1,
                 ymax_animals=None,
                 cmax_animals=None,
                 hist_specs=None,
                 img_dir=None,
                 img_base=None,
                 img_fmt='png',
                 img_years=None,
                 log_file=None):
        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal densities
        :param hist_specs: Specifications for histograms, see below
        :param vis_years: years between visualization updates (if 0, disable graphics)
        :param img_dir: String with path to directory for figures
        :param img_base: String with beginning of file name for figures
        :param img_fmt: String with file type for figures, e.g. 'png'
        :param img_years: years between visualizations saved to files (default: vis_years)
        :param log_file: If given, write animal counts to this file

        If ymax_animals is None, the y-axis limit should be adjusted automatically.
        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
           {'Herbivore': 50, 'Carnivore': 20}

        hist_specs is a dictionary with one entry per property for which a histogram shall be shown.
        For each property, a dictionary providing the maximum value and the bin width must be
        given, e.g.,
            {'weight': {'max': 80, 'delta': 2}, 'fitness': {'max': 1.0, 'delta': 0.05}}
        Permitted properties are 'weight', 'age', 'fitness'.

        If img_dir is None, no figures are written to file. Filenames are formed as

            f'{os.path.join(img_dir, img_base}_{img_number:05d}.{img_fmt}'

        where img_number are consecutive image numbers starting from 0.

        img_dir and img_base must either be both None or both strings.
        """
        random.seed(seed)

        if img_years is None:
            self.img_years = vis_years

        self.vis_years = vis_years

        self.current_year = 0
        self.final_year = None

        self.island_map = island_map
        self.island = Island(island_map, ini_pop)

        if img_dir is None:
            self.img_base = None
        else:
            self.img_base = os.path.join(img_dir, _DEFAULT_GRAPHICS_NAME)

        self.img_fmt = img_fmt

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        if species == "Herbivore":
            Herbivores.set_params(params)
        elif species == "Carnivore":
            Carnivores.set_params(params)

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        if landscape == 'L':
            Lowland.set_params(params)
        elif landscape == 'H':
            Highland.set_params(params)
        elif landscape == 'D':
            Desert.set_params(params)
        elif landscape == 'W':
            Water.set_params(params)

    def simulate(self, num_years):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        """
        self.final_year = self.current_year + num_years

        while self.current_year < self.final_year:
            self.island.annual_cycle_simulation()

            # Add visualization if tests later

        self.current_year += 1

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """
        self.island.adding_population(population)

    @property
    def year(self):
        """Last year simulated."""
        pass

    @property
    def num_animals(self):
        """Total number of animals on island."""
        pass

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        pass

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""
        pass
