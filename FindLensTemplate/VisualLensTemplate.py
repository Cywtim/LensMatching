import numpy as np
import cv2 as cv
import os
from astropy.io import fits
from matplotlib import pyplot as plt
from FindLensTemplate import FindLensTemplate

class VisualTemp:
    def __init__(self, data_dir, position_dict, w, h, ncols, nrows, figsize=(8, 6), **kwargs):

        self.data_dir = data_dir
        self.position_dict = position_dict
        self.len = len(position_dict)
        self.w = w
        self.h = h
        self.ncols = ncols
        self.nrows = nrows
        self.figsize = figsize
        self.fig, self.ax = plt.subplots(nrows, ncols, figsize, **kwargs)

        if self.len > (self.ncols*self.nrows):
            print("The lens of position dictionary is out of range of subplots.")
            exit()

    def __iter__(self):
        for sub in (self.fig, self.ax):
            yield sub

    def ShowSubplots(self, cmap="rainbow", dotcolor="red"):

        file_name_list = list(self.position_dict)
        psotion_list = list(self.position_dict.values())

        for r in range(self.nrows):
            for c in range(self.ncols):
                image = fits.open(os.path.join(self.data_dir,
                            file_name_list[r+c]))
                img = self.ax[r, c].imshow(image, cmap=cmap)
                self.ax.scatter(psotion_list[r+c], color=dotcolor)
                plt.title(file_name_list[r+c])
                self.fig.colorbar(img)
        plt.show()



