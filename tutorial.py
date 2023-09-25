import numpy as np
import cv2 as cv
from numpy import cos, sin
from astropy.io import fits
from astropy import units,constants
from matplotlib import pyplot as plt
from FindLensTemplate.FindLensTemplate import FindLensTemplate

"""
It requires a file structure like:
LensMatching/
    |
    |---FindLensTemplate package
    |
    ----dataset/
            |
            |---Template/
            |      |
            |      |----Template.fits
            |
            ----coadd_DESJ2125-6504/
                    |
                    ----coadd_DESJ2125-6504_g.fits
                    |
                    ----coadd_DESJ2125-6504_r.fits
                    |
                    ----coadd_DESJ2125-6504_i.fits
"""



#%%
"""
Initialize the FindLensTemplate class
The image directory is "dataset/coadd_DESJ2125-6504"
THe name of template is "Template.fits"
"""
coadd_DESJ2125_6504_find = FindLensTemplate("dataset/coadd_DESJ2125-6504",
                                            "coadd_DESJ2125-6504",
                                            "dataset/Template/coadd_DESJ2125-6504_template.fits")
#%%

"""
Use the MulFilMathch to obtain the most likely position of the same pattern as Template.
"""
position = coadd_DESJ2125_6504_find.MulFileMatch(progress=10)

"""
Print the most likely position in turns.
"""
print(position)