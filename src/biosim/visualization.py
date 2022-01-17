
__author__ = 'Andrine Zimmermann, Karin Mollatt'
__email__ = 'andrine.zimmermann@nmbu.no, karin.mollatt@nmbu.no'

"""
Module for visualization graphics of Rossumøya.


:mod:`biosim.visualization` provides graphics support for BioSim.

.. note::
   * This module requires the program ``ffmpeg`` or ``convert``
     available from `<https://ffmpeg.org>` and `<https://imagemagick.org>`.
   * You can also install ``ffmpeg`` using ``conda install ffmpeg``
   * You need to set the  :const:`_FFMPEG_BINARY` and :const:`_CONVERT_BINARY`
     constants below to the command required to invoke the programs
   * You need to set the :const:`_DEFAULT_FILEBASE` constant below to the
     directory and file-name start you want to use for the graphics output
     files.

This file is based on and very much inspired by Plesser, H.E.
"""

import matplotlib.pyplot as plt
import numpy as np
import subprocess
import os

# Update these variables to point to your ffmpeg and convert binaries
# If you installed ffmpeg using conda or installed both softwares in
# standard ways on your computer, no changes should be required.
_FFMPEG_BINARY = 'ffmpeg'
_MAGICK_BINARY = 'magick'

# update this to the directory and file-name beginning
# for the graphics files
_DEFAULT_GRAPHICS_DIR = os.path.join('../..', 'data')
_DEFAULT_GRAPHICS_NAME = 'bs'
_DEFAULT_IMG_FORMAT = 'png'
_DEFAULT_MOVIE_FORMAT = 'mp4'   # alternatives: mp4, gif


class Graphics:
    """
    Provides graphics support for BioSim
    """

    def __init__(self, img_dir=None, img_name=None, img_fmt=None):
        """
        :param img_dir: directory for image files; no images if None
        :type img_dir: str
        :param img_name: beginning of name for image files
        :type img_name: str
        :param img_fmt: image file format suffix
        :type img_fmt: str
        """
        if img_name is None:
            img_name = _DEFAULT_GRAPHICS_NAME

        if img_dir is not None:
            self._img_base = os.path.join(img_dir, img_name)
        else:
            self._img_base = None

        self._img_fmt = img_fmt if img_fmt is not None else _DEFAULT_IMG_FORMAT

        self._img_ctr = 0
        self._img_step = 1

        # the following will be initialized by _setup_graphics
        self._fig = None
        self._map_ax = None
        self._img_axis = None
        self._mean_ax = None

        self._mean_line_herb = None
        self._mean_line_carn = None

        self._year_ax = None
        self._year_text = None

        self._herb_ax = None
        self._herb_axis = None
        self._carn_ax = None
        self._carn_axis = None

        self._fitness_ax = None
        self._fitness_axis = None
        self._age_ax = None
        self._age_axis = None
        self._weight_ax = None
        self._weight_axis = None

        self._gridspec = None

    def update(self, sys_map, herb_array, carn_array, cmax_herb, cmax_carn, amount_animals_species, year):
        """
        Updates graphics with current data and save to file if necessary.

        :param sys_map: current system status (2d array)
        :param amount_animals_species: amount of animals per species
        :param year: current year
        """

        self._update_system_map(sys_map)
        self._update_herb_heatmap(herb_array, cmax_herb)
        self._update_carn_heatmap(carn_array, cmax_carn)
        self._update_year(year)
        self._update_mean_graph(amount_animals_species, year)
        self._fig.canvas.flush_events()  # ensure every thing is drawn
        plt.pause(0.00001)  # pause required to pass control to GUI

        #self._save_graphics(step)

    def make_movie(self, movie_fmt=None):
        """
        Creates MPEG4 movie from visualization images saved.

        .. :note:
            Requires ffmpeg for MP4 and magick for GIF

        The movie is stored as img_base + movie_fmt
        """
        if self._img_base is None:
            raise RuntimeError("No filename defined.")

        if movie_fmt is None:
            movie_fmt = _DEFAULT_MOVIE_FORMAT

        if movie_fmt == 'mp4':
            try:
                # Parameters chosen according to http://trac.ffmpeg.org/wiki/Encode/H.264,
                # section "Compatibility"
                subprocess.check_call([_FFMPEG_BINARY,
                                       '-i', '{}_%05d.png'.format(self._img_base),
                                       '-y',
                                       '-profile:v', 'baseline',
                                       '-level', '3.0',
                                       '-pix_fmt', 'yuv420p',
                                       '{}.{}'.format(self._img_base, movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: ffmpeg failed with: {}'.format(err))
        elif movie_fmt == 'gif':
            try:
                subprocess.check_call([_MAGICK_BINARY,
                                       '-delay', '1',
                                       '-loop', '0',
                                       '{}_*.png'.format(self._img_base),
                                       '{}.{}'.format(self._img_base, movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: convert failed with: {}'.format(err))
        else:
            raise ValueError('Unknown movie format: ' + movie_fmt)

    def _setup_graphics(self, y_lim, final_year, img_step, current_year):
        """
        Prepare graphics.

        Call this before calling :meth:`update()` for the first time after
        the final time step has changed.

        :param y_lim: upper limit of y-axis
        :param final_year: last time step to be visualised (upper limit of x-axis)
        :param img_step: interval between saving image to file
        """
        self._img_step = img_step

        # Create new figure window
        if self._fig is None:
            self._fig = plt.figure(constrained_layout=True, figsize=(10, 8))
            self._gridspec = self._fig.add_gridspec(9,18)
            plt.axis('off')

        # Subplot for island map
        if self._map_ax is None:
            self._map_ax = self._fig.add_subplot(self._gridspec[:3, :4])
            self._img_axis = None
            #self._map_ax.set_xticks()
            #self._map_ax.set_xticklabels([])
            #self._map_ax.set_yticks()
            #self._map_ax.set_yticklabels([])
            self._map_ax.title.set_text('Island')

        # Subplot for current year
        if self._year_ax is None:
            self._year_ax = self._fig.add_subplot(self._gridspec[:3, 6:12])
            self._year_text = self._year_ax.text(0.5, 0.5,
                                                 f'Year: {current_year}',
                                                 horizontalalignment='center',
                                                 verticalalignment='center',
                                                 transform=self._year_ax.transAxes,
                                                 fontsize=16)
            self._year_ax.axis('off')

        # Subplot for amount of animals per species
        if self._mean_ax is None:
            self._mean_ax = self._fig.add_subplot(self._gridspec[:3, 12:18])
            self._mean_ax.set_xlim(0, final_year + 1)
            self._mean_ax.set_ylim(0, y_lim)
            self._mean_ax.title.set_text('Animal count')
            self._mean_ax.set_box_aspect(1)
        elif self._mean_ax is not None:
            self._mean_ax.set_xlim(0, final_year + 1)

        # Subplot for herbivore heatmap
        if self._herb_ax is None:
            self._herb_ax = self._fig.add_subplot(self._gridspec[4:7, 2:8])
            self._herb_axis = None
            self._herb_ax.title.set_text('Herbivore distribution')

        # Subplot for carnivore heatmap
        if self._carn_ax is None:
            self._carn_ax = self._fig.add_subplot(self._gridspec[4:7, 10:16])
            self._carn_axis = None
            self._carn_ax.title.set_text('Carnivore distribution')

        # Subplot for fitness histogram
        if self._fitness_ax is None:
            self._fitness_ax = self._fig.add_subplot(self._gridspec[8:, 1:6])
            self._fitness_axis = None
            self._fitness_ax.set_title('Fitness')

        # Subplot for age histogram
        if self._age_ax is None:
            self._age_ax = self._fig.add_subplot(self._gridspec[8:, 7:12])
            self._age_ax.set_title('Age')

        # Subplot for weight histogram
        if self._weight_ax is None:
            self._weight_ax = self._fig.add_subplot(self._gridspec[8:, 13:18])
            self._weight_ax.set_title('Weight')

        # Graph line for herbivores
        if self._mean_line_herb is None:
            mean_plot_herb = self._mean_ax.plot(np.arange(0, final_year + 1),
                                           np.full(final_year + 1, np.nan), label='Herbivore')
            self._mean_line_herb = mean_plot_herb[0]
        else:
            x_data, y_data = self._mean_line_herb.get_data()
            x_new = np.arange(x_data[-1] + 1, final_year + 1)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self._mean_line_herb.set_data(np.hstack((x_data, x_new)),
                                              np.hstack((y_data, y_new)))

        # Graph line for herbivores
        if self._mean_line_carn is None:
            mean_plot_carn = self._mean_ax.plot(np.arange(0, final_year + 1),
                                                np.full(final_year + 1, np.nan), label='Carnivore')
            self._mean_line_carn = mean_plot_carn[0]
        else:
            x_data, y_data = self._mean_line_carn.get_data()
            x_new = np.arange(x_data[-1] + 1, final_year + 1)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self._mean_line_carn.set_data(np.hstack((x_data, x_new)),
                                              np.hstack((y_data, y_new)))

    def _update_system_map(self, sys_map):
        """
        Method for updating the island map.
        """
        #                   R    G    B
        rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
                     'L': (0.0, 0.6, 0.0),  # dark green
                     'H': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow

        map_rgb = [[rgb_value[column] for column in row]
                   for row in sys_map.splitlines()]

        if self._img_axis is not None:
            self._img_axis.set_data(map_rgb)
        else:
            self._img_axis = self._map_ax.imshow(map_rgb,
                                                 interpolation='nearest')

        # This next part is picked up from Plesser, H.E. file 'mapping.py' from
        # https://gitlab.com/nmbu.no/emner/inf200/h2021/inf200-course-materials/-/blob/
        # main/january_block/examples/plotting/mapping.py
        ax_lg = self._fig.add_subplot(self._gridspec[:2, 5:6])
        ax_lg.axis('off')
        for ix, name in enumerate(('Water', 'Lowland',
                                   'Highland', 'Desert')):
            ax_lg.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1,
                                          edgecolor='none',
                                          facecolor=rgb_value[name[0]]))
            ax_lg.text(0.35, ix * 0.2, name, transform=ax_lg.transAxes)

    def _update_year(self, current_year):
        """
        Method for updating current year.

        :param current_year: The current year on the island.
        """
        self._year_text.set_text(f'Year: {current_year}')

    def _update_herb_heatmap(self, herb_array, cmax):
        """
        Method for updating heatmap for herbivores.

        :param sys_map: multiline string specifying island geography
        """
        if self._herb_axis is not None:
            self._herb_axis.set_data(herb_array)
        else:
            self._herb_axis = self._herb_ax.imshow(herb_array, interpolation='nearest', vmin=0, vmax=cmax)
            plt.colorbar(self._herb_axis, ax=self._herb_ax, orientation='vertical')

    def _update_carn_heatmap(self, carn_array, cmax):
        """
        Method for updating heatmap for herbivores.

        :param sys_map: multiline string specifying island geography
        """
        if self._carn_axis is not None:
            self._carn_axis.set_data(carn_array)
        else:
            self._carn_axis = self._carn_ax.imshow(carn_array, interpolation='nearest', vmin=0, vmax=cmax)
            plt.colorbar(self._carn_axis, ax=self._carn_ax, orientation='vertical')

    def _update_fitness_hist(self, herb_list=None, carn_list=None, hist_specs=None):
        """
        Method for updating the fitness histogram.

        :param herb_list: List with fitness for herbivores
        :param carn_list: List with fitness for carnivores
        :param hist_specs: Specifications for histograms
        """
        if hist_specs is None:
            self._fitness_ax.clear()
            self._fitness_ax.hist(herb_list, histtype='step', color='b')
            self._fitness_ax.hist(carn_list, histtype='step', color='r')
            self._fitness_ax.title.set_text('Fitness')
        else:
            fit_bins = (int(hist_specs["fitness"]["max"] / hist_specs["fitness"]["delta"]))
            self._fitness_ax.clear()
            self._fitness_ax.hist(herb_list, bins=fit_bins, histtype='step', color='b',
                                    range=(0, hist_specs["fitness"]["max"]))
            self._fitness_ax.hist(carn_list, bins=fit_bins, histtype='step', color='r',
                                    range=(0, hist_specs["fitness"]["max"]))
            self._fitness_ax.title.set_text('Fitness')

    def _update_age_hist(self, herb_list=None, carn_list=None, hist_specs=None):
        """
        Method for updating the age histogram.

        :param herb_list: List with age for herbivores
        :param carn_list: List with age for carnivores
        :param hist_specs: Specifications for histograms
        """
        if hist_specs is None:
            self._age_ax.clear()
            self._age_ax.hist(herb_list, histtype='step', color='b')
            self._age_ax.hist(carn_list, histtype='step', color='r')
            self._age_ax.title.set_text('Age')
        else:
            age_bins = (int(hist_specs["age"]["max"] / hist_specs["age"]["delta"]))
            self._age_ax.clear()
            self._age_ax.hist(herb_list, bins=age_bins, histtype='step', color='b',
                              range=(0, hist_specs["age"]["max"]))
            self._age_ax.hist(carn_list, bins=age_bins, histtype='step', color='r',
                              range=(0, hist_specs["age"]["max"]))
            self._age_ax.title.set_text('Age')

    def _update_weight_hist(self, herb_list=None, carn_list=None, hist_specs=None):
        """
        Method for updating the weight histogram.

        :param herb_list: List with weight for herbivores
        :param carn_list: List with weight for carnivores
        :param hist_specs: Specifications for histograms
        """
        if hist_specs is None:
            self._weight_ax.clear()
            self._weight_ax.hist(herb_list, histtype='step', color='b')
            self._weight_ax.hist(carn_list, histtype='step', color='r')
            self._weight_ax.title.set_text('Weight')
        else:
            weight_bins = (int(hist_specs["weight"]["max"] / hist_specs["weight"]["delta"]))
            self._weight_ax.clear()
            self._weight_ax.hist(herb_list, bins=weight_bins, histtype='step', color='b',
                              range=(0, hist_specs["weight"]["max"]))
            self._weight_ax.hist(carn_list, bins=weight_bins, histtype='step', color='r',
                              range=(0, hist_specs["weight"]["max"]))
            self._weight_ax.title.set_text('Weight')

    def _update_mean_graph(self, amount_animals_species, year):
        """
        Method for updating the graphs for amount of animals per species.

        :param amount_animals_species: Dictionary containing amount of animals per species.
        :param year: Current year
        """
        amount_herbs = amount_animals_species['Herbivores']
        amount_carns = amount_animals_species['Carnivores']

        y_data_herb = self._mean_line_herb.get_ydata()
        y_data_herb[year] = amount_herbs
        self._mean_line_herb.set_ydata(y_data_herb)

        """if self._mean_ax.get_ylim()[1] < amount_herbs:
            self._mean_ax.autoscale(enable=True, axis='y')"""

        y_data_carn = self._mean_line_carn.get_ydata()
        y_data_carn[year] = amount_carns
        self._mean_line_carn.set_ydata(y_data_carn)

    def _save_graphics(self, step):
        """Saves graphics to file if file name given."""

        if self._img_base is None or step % self._img_step != 0:
            return

        plt.savefig('{base}_{num:04d}.{type}'.format(base=self._img_base,
                                                     num=self._img_ctr,
                                                     type=self._img_fmt))
        self._img_ctr += 1
