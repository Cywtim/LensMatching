import numpy as np
import cv2 as cv
from numpy import cos, sin
from astropy.io import fits
from astropy import units,constants
from matplotlib import pyplot as plt
from FindLensTemplate.FindLensTemplate import FindLensTemplate



coadd_DESJ2125_6504_find = FindLensTemplate("dataset/coadd_DESJ2125-6504", "Template.fits")

position = coadd_DESJ2125_6504_find.MulFileMatch()

print("finished")