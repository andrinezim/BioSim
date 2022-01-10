
__author__ = 'Andrine Zimmermann, Karin Mollatt'
__email__ = 'andrine.zimmermann@nmbu.no, karin.mollatt@nmbu.no'

"""
Module for visualization graphics of Rossumøya.
"""

import matplotlib.pyplot as plt
import os
import numpy as np


_DEFAULT_GRAPHICS_NAME = 'bio'
_DEFAULT_IMG_FORMAT = "png"


class Visualization:
    """
    Class for providing graphics for visualization of BioSim.
    """

    def __init__(self, img_dir=None, img_name=None, img_fmt=None):
        """
        Method for saving values in class.

        :param img_dir: String with path to directory for figures
        :param img_name: String with beginning of file name for figures
        :param img_fmt: String with file type for figures, e.g. 'png'
        """
        if img_name is None:
            img_name = _DEFAULT_GRAPHICS_NAME

        if img_dir is not None:
            self._img_base = os.path.join(img_dir, img_name)
        else:
            self._img_base = None

        self._img_fmt = img_fmt if img_fmt is not None else _DEFAULT_IMG_FORMAT

        # self._img_ctr = 0
        # self._img_step = 1

        # The following will be initialized by _setup_graphics
        self._fig = None
        self._map_ax = None
        self._img_axis = None
        self._mean_ax = None
        self._mean_line = None

    def update(self, step, sys_map, sys_mean):
        """
        Updates graphics with current data and save to file if necessary.

        :param step: current time step
        :param sys_map: current system status (2D array)
        :param sys_mean: current mean value of system
        :return:
        """

        self._update_system_map(sys_map)
        self._update_mean_graph(step, sys_mean)
        self._fig.canvas.flush_events()  # ensure every thing is drawn
        plt.pause(0.01)  # pause required to pass control to GUI

        self._save_graphics(step)

    def make_movie(self):
        pass

    def _setup_graphics(self, final_step, img_step):
        """
        Method for setting up the graphics.

        :param final_step: last time-step to be visualized. (Upper limit of x-axis.)
        :param img_step: interval between saving image to file.
        """

        self._img_step = img_step

        # Create new figure window
        if self._fig is None:
            self._fig = plt.figure()

        # Add right subplot for line graph of mean.
        if self._mean_ax is None:
            self._mean_ax = self._fig.add_subplot(1, 2, 2)
            self._mean_ax.set_ylim(-0.05, 0.05)

        # Needs updating on subsequent calls to simulate().
        # Add 1 so we can show values for time zero and time final_step.
        self._mean_ax.set_xlim(0, final_step + 1)

        if self._mean_line is None:
            mean_plot = self._mean_ax.plot(np.arange(0, final_step + 1),
                                           np.full(final_step + 1, np.nan))
            self._mean_line = mean_plot[0]
        else:
            x_data, y_data = self._mean_line.get_data()
            x_new = np.arange(x_data[-1] + 1, final_step + 1)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self._mean_line.set_data(np.hstack((x_data, x_new)),
                                         np.hstack((y_data, y_new)))

    def _update_system_map(self):
        pass

    def _update_mean_graph(self):
        pass

    def _save_graphics(self):
        pass

