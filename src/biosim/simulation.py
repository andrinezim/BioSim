
__author__ = 'Andrine Zimmermann, Karin Mollatt'
__email__ = 'andrine.zimmermann@nmbu.no, karin.mollatt@nmbu.no'

"""
Template for BioSim class.
"""

# The material in this file is licensed under the BSD 3-clause license
# https://opensource.org/licenses/BSD-3-Clause
# (C) Copyright 2021 Hans Ekkehard Plesser / NMBU

from .landscapes import Lowland, Highland, Desert, Water
from .animals import Herbivores, Carnivores
from .visualization import Graphics
from .island import Island
import random
import os

_DEFAULT_GRAPHICS_NAME = 'bs'


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
        else:
            self.img_years = vis_years

        self.vis_years = vis_years

        self._current_year = 0
        self._final_year = None

        self.island_map = island_map
        self.island = Island(island_map, ini_pop)

        if img_dir is None:
            self.img_base = None
        else:
            self.img_base = os.path.join(img_dir, _DEFAULT_GRAPHICS_NAME)

        self.img_fmt = img_fmt

        self._graphics = Graphics(img_dir, img_base, img_fmt)

        if ymax_animals is None:
            self.ymax_animals = 6000
        else:
            self.ymax_animals = ymax_animals

        if cmax_animals is None:
            self.cmax_herb = 50
            self.cmax_carn = 20
        else:
            self.cmax_herb = cmax_animals['Herbivore']
            self.cmax_carn = cmax_animals['Carnivore']

        self.hist_specs = hist_specs

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        self.island.set_animal_params_island(species, params)

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
        enable_graphics = True

        self._final_year = self._current_year + num_years
        if self.vis_years != 0:
            self._graphics._setup_graphics(self.ymax_animals, self._final_year, self.img_years, self._current_year,
                                           self.island.row_length, self.island.col_length)
            self._graphics._update_system_map(self.island_map)
            if self.img_years % self.vis_years != 0:
                raise ValueError('img_years must be multiple of vis_years')
        else:
            enable_graphics = False
            self.vis_years = 1

        while self._current_year < self._final_year:
            self.island.annual_cycle_simulation()
            self._current_year += 1

            if self._current_year % self.vis_years == 0 and enable_graphics:
                self._graphics.update(self.island_map,
                                      self.island.heatmap_population()[0],
                                      self.island.heatmap_population()[1],
                                      self.cmax_herb,
                                      self.cmax_carn,
                                      self.num_animals_per_species,
                                      self._current_year)
                self._graphics._update_fitness_hist(self.island.fitness_list()[0],
                                                    self.island.fitness_list()[1],
                                                    self.hist_specs)
                self._graphics._update_age_hist(self.island.age_list()[0],
                                                    self.island.age_list()[1],
                                                    self.hist_specs)
                self._graphics._update_weight_hist(self.island.weight_list()[0],
                                                    self.island.weight_list()[1],
                                                    self.hist_specs)

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """
        self.island.adding_population(population)

    @property
    def year(self):
        """
        Last year simulated.
        """
        return self._current_year

    @property
    def num_animals(self):
        """
        Total number of animals on island.
        """
        _ , total_amount_animals = self.island.animals_per_species()
        return total_amount_animals

    @property
    def num_animals_per_species(self):
        """
        Number of animals per species in island, as dictionary.
        """
        amount_animals_species, _ = self.island.animals_per_species()
        return amount_animals_species

    def make_movie(self):
        """
        Create MPEG4 movie from visualization images saved.
        """
        pass

    def save_graphics(self):
        pass
