
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

    def update(self, sys_map, amount_animals_species, step):
        """
        Updates graphics with current data and save to file if necessary.

        :param step: current time step
        :param sys_map: current system status (2d array)
        :param sys_mean: current mean value of system
        """

        self._update_system_map(sys_map)
        self._update_mean_graph(amount_animals_species, step)
        self._fig.canvas.flush_events()  # ensure every thing is drawn
        plt.pause(0.001)  # pause required to pass control to GUI

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

    def _setup_graphics(self, y_lim, final_year, img_step):
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
            self._fig = plt.figure()
            plt.axis('off')

        # Subplot for island map
        if self._map_ax is None:
            self._map_ax = self._fig.add_subplot(1, 2, 1)
            self._img_axis = None
            self._map_ax.title.set_text('Island')

        # Subplot for amount of animals per species
        if self._mean_ax is None:
            self._mean_ax = self._fig.add_subplot(1, 2, 2)
            self._mean_ax.set_ylim(0, y_lim)
            self._mean_ax.title.set_text('Amount of animals per species')
            self._mean_ax.set_box_aspect(1)

        # Needs updating on subsequent calls to simulate()
        # Add 1 so we can show values for time zero and time final_step
        self._mean_ax.set_xlim(0, final_year + 1)

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
