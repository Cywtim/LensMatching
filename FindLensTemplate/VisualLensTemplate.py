import numpy as np
import cv2 as cv
import os
from astropy.io import fits
from matplotlib import pyplot as plt
from FindLensTemplate import FindLensTemplate

class VisualTemp:
    def __init__(self, data_dir, position_dict, ncols, nrows, w=50, h=50, **kwargs):

        self.data_dir = data_dir
        self.position_dict = position_dict
        self.len = len(position_dict)
        self.w = w
        self.h = h
        self.ncols = ncols
        self.nrows = nrows

        if self.len > (self.ncols*self.nrows):
            print("Error, The lens of position dictionary is out of range of subplots.")
            exit()

    def ShowSubplots(self, cmap="rainbow", figsize=(8, 6)):

        file_name_list = list(self.position_dict)
        position_list = list(self.position_dict.values())

        fig, ax = plt.subplots(self.nrows, self.ncols, figsize=figsize)

        for r in range(self.nrows):
            for c in range(self.ncols):
                try:
                    image = fits.open(os.path.join(self.data_dir,
                                file_name_list[c+self.ncols*r]))
                    image = image[0].data
                    position = position_list[c+self.ncols*r]
                    img = ax[r, c].imshow(image[position[1]:position[1]+self.w,
                                    position[0]:position[0]+self.h], cmap=cmap)
                    ax[r, c].set_title(file_name_list[c+self.ncols*r])
                    fig.colorbar(img)
                except:
                    pass
        fig.show()

        return fig, ax


    def ShowPosition(self, cmap="rainbow", dotcolor="red", figsize=(6, 10)):

        file_name_list = list(self.position_dict)
        position_list = list(self.position_dict.values())

        fig, ax = plt.subplots(self.nrows, self.ncols, figsize=figsize)

        for r in range(self.nrows):
            for c in range(self.ncols):
                try:
                    image = fits.open(os.path.join(self.data_dir,
                                file_name_list[c+self.ncols*r]))
                    image = image[0].data
                    position = position_list[c+self.ncols*r]
                    img = ax[r, c].imshow(image, cmap=cmap)
                    ax[r, c].scatter(position[1], position[0], color=dotcolor)
                    ax[r, c].set_title(file_name_list[c+self.ncols*r])

                except:
                    pass
        fig.show()

        return fig, ax


