import numpy as np
import cv2 as cv
import os
from astropy.io import fits
from matplotlib import pyplot as plt
from FindLensTemplate import FindLensTemplate

class VisualTemp:
    def __init__(self, data_dir, position_dict, ncols, nrows, w=50, h=50, figsize=(8, 6), **kwargs):

        self.data_dir = data_dir
        self.position_dict = position_dict
        self.len = len(position_dict)
        self.w = w
        self.h = h
        self.ncols = ncols
        self.nrows = nrows
        self.figsize = figsize

        if self.len > (self.ncols*self.nrows):
            print("Error, The lens of position dictionary is out of range of subplots.")
            exit()

    def ShowSubplots(self, cmap="rainbow", dotcolor="red"):

        file_name_list = list(self.position_dict)
        position_list = list(self.position_dict.values())

        fig, ax = plt.subplots(self.nrows, self.ncols, figsize=self.figsize)

        for r in range(self.nrows):
            for c in range(self.ncols):
                image = fits.open(os.path.join(self.data_dir,
                            file_name_list[r+c]))
                image = image[0].data
                position = position_list[r+c]
                img = ax[r, c].imshow(image[position[1]:position[1]+self.w,
                                position[0]:position[0]+self.h], cmap=cmap)
                plt.title(file_name_list[r+c])
                fig.colorbar(img)
        fig.show()

        return fig, ax


