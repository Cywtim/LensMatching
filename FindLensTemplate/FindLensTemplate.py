import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
import os
from astropy.io import fits


class FindLensTemplate:

    def __init__(self, image_dir, temp_name,matchTemplate=cv.matchTemplate,method=cv.TM_CCOEFF_NORMED, isMax=True, scale="log"):

        self.image_dir = image_dir
        self.temp_name = temp_name
        self.method = method
        self.isMax = isMax
        self.scale = scale
        self.matchTemplate = matchTemplate

        if scale == "linear":
            self.scaler = eval("np.array")
        elif scale == "power":
            self.scaler = eval("np.square")
        else:
            try:
                self.scaler = eval("np." + scale)
            except:
                self.print("scale is not a numpy function.")



    def MethodMatch(self, image_path, temp):

        """

        :param image_path: str,
        :param temp:
        :param method:
        :param isMax:
        :return:
        """

        # open the image fits file and rescale/normalize the image
        image_file = fits.open(image_path)
        image = image_file[0].data
        image_min = image.min()
        image = image - image_min * (1 - np.sign(image_min) * 0.001)
        image = self.scaler(image)
        image_min = image.min()
        image_max = image.max()
        image = (image - image_min) / (image_max - image_min) * 255
        img = image.copy()

        # Apply template Matching
        if isinstance(temp, str):
            template = fits.open(temp)[0].data
            res = self.matchTemplate(img, template, method=self.method)

        elif isinstance(temp, np.ndarray):

            res = cv.matchTemplate(img, temp, method=self.method)

        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

        if self.isMax:
            return max_loc
        else:
            return min_loc

    def MulFileMatch(self):
        """

        :param image_dir:
        :param temp_name:
        :param args:
        :param kwargs:
        :return:
        """

        temp_path = os.path.join(self.image_dir, self.temp_name)
        template = fits.open(temp_path)[0].data

        position_list = []

        for file_name in os.listdir(self.image_dir):
            if file_name != self.temp_name:

                file_path = os.path.join(self.image_dir, file_name)
                print(file_path)

                position = self.MethodMatch(file_path, template)

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
