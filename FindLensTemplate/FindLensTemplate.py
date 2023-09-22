import numpy as np
import cv2 as cv
from astropy.io import fits


class FindLensTemplate():

    def __int__(self, target_path):

        self.image_path_list = target_path

    def MethodMathch(self, image_path, temp, method=cv.TM_CCOEFF_NORMED, isMax=True):

        # open the image fits file
        image_file = fits.open(image_path)
        image = image_file[0].data
        img = image.copy()

        # Apply template Matching
        if isinstance(temp, str):
            temp = fits.open(temp)[0].data
            res = cv.matchTemplate(img, temp, method=method)

        elif isinstance(temp, np.ndarray):

            res = cv.matchTemplate(img, temp, method=method)

        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

        if isMax:
            return max_loc
        else:
            return min_loc

    def MethodMathch(self, image_path, temp, method=cv.TM_CCOEFF_NORMED, isMax=True):

        """
        A simple template matching gravitational lens
        :param image_path: the image path
        :param temp:
        :param method:
        :param isMax:
        :return:
        """

        # open the image fits file
        image_file = fits.open(image_path)
        image = image_file[0].data
        img = image.copy()

        # Apply template Matching
        if isinstance(temp, str):
            temp = fits.open(temp)[0].data
            res = cv.matchTemplate(img, temp, method=method)

        elif isinstance(temp, np.ndarray):

            res = cv.matchTemplate(img, temp, method=method)

        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

        if isMax:
            return max_loc
        else:
            return min_loc

    def MulMethodMatch(self, image, temp, methods=None, isMax=True):

        if methods is None:
            methods = [cv.TM_CCOEFF_NORMED]

        res_ms = []

        img = image.copy()

        for method in methods:
            res_m = cv.matchTemplate(img, temp, method=method)

            res_ms.append(res_m)

        res_ms = np.array(res_ms)

        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res_ms)

        if isMax:
            return max_loc
        else:
            return min_loc
