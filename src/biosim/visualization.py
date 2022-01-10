
__author__ = 'Andrine Zimmermann, Karin Mollatt'
__email__ = 'andrine.zimmermann@nmbu.no, karin.mollatt@nmbu.no'

"""
Module for visualization graphics of Rossumøya.
"""

import matplotlib.pyplot as plt
import os


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


