import numpy as np
import cv2 as cv
import os
from astropy.io import fits


class FindLensTemplate():

    def __int__(self, target_path):

        self.image_path_list = target_path

    def MethodMathch(self, image_path, temp, method=cv.TM_CCOEFF_NORMED, isMax=True):

        """

        :param image_path:
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

    def MulFileMatch(self, image_dir, temp_name="Template.fits", *args, **kwargs):
        """

        :param image_dir:
        :param temp_name:
        :param args:
        :param kwargs:
        :return:
        """

        temp_path = os.path.join(image_dir, temp_name)

        position_list = []

        for file_name in os.listdir(image_dir):

            if file_name != temp_name:

                file_path = os.path.join(image_dir, file_name)

                position = self.MulFileMatch(file_path, temp_path, kwargs)

                position_list.append(position)

        return np.array(position_list)

    def MulMethodMatch(self, image, temp, methods=None, isMax=True):
        """

        :param image:
        :param temp:
        :param methods:
        :param isMax:
        :return:
        """

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
