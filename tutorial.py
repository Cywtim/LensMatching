#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
import numpy as np
import cv2 as cv
from numpy import cos, sin
from astropy.io import fits
from astropy import units,constants
from matplotlib import pyplot as plt
from FindLensTemplate.FindLensTemplate import FindLensTemplate
from FindLensTemplate.VisualLensTemplate import VisualTemp

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
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
            |      |---coadd_DESJ2125-6504_Template.fits
            |
            ----data4/
                  |
                  |----coadd_DESJ2125-6504_g.fits
                  |
                  |----coadd_DESJ2125-6504_r.fits
                  |
                  |----coadd_DESJ2125-6504_i.fits
"""
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
Initialize the FindLensTemplate class
The image directory is "dataset/data"
The images' prefix is "coadd_DESJ2125-6504"
THe name of template is "coadd_DESJ2125-6504_template.fits"
"""
coadd_DESJ2125_6504_find = FindLensTemplate(
    "dataset/data",  "coadd_DESJ2125-6504",
    "dataset/Template/coadd_DESJ2125-6504_template.fits"
)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

"""
Use the MulFilMathch to obtain the most likely position of the same pattern as Template.
"""
position_dict = coadd_DESJ2125_6504_find.MulFileMatch(progress=8, prefix=2)

"""
Print the most likely position in turns.
"""
print(position_dict)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
Show the images and found lens positions.
"""
Visual = VisualTemp("dataset/data",
                      position_dict,
                      w=50, h=50,
                      ncols=2,nrows=2,
                      figsize=(10,10))
