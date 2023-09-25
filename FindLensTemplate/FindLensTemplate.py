import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
import os
import sys
from astropy.io import fits


class FindLensTemplate:

    def __init__(self, image_dir, temp_name,
                 matchTemplate=cv.matchTemplate,
                 method=cv.TM_CCOEFF_NORMED,
                 isMax=True, rescale="log",
                 ndtype="float32"):
        """
        This module is to find similar patterns between different band of same lensing fields
        :param image_dir: str, the directory of image lists
        :param temp_name: str, the name of template or template image in the same directory of images
        :param matchTemplate: callable, matching function
        :param method: None, the parameters of function
        :param isMax: Bool, output the maximum or minimum result of matching, default is True
        :param rescale: str, mathematical functions from numpy to rescale the images.
        """
        self.image_dir = image_dir
        self.temp_name = temp_name
        self.method = method
        self.isMax = isMax
        self.rescale = rescale
        self.matchTemplate = matchTemplate
        self.ndtype = ndtype

        if rescale == "linear":
            self.rescaler = eval("np.array")
        elif rescale == "power":
            self.rescaler = eval("np.square")
        else:
            try:
                self.rescaler = eval("np." + self.rescale)
            except:
                print("scale is not a numpy function.")



    def MethodMatch(self, image_path, temp):

        """
        Find the most similar temp pattern in single image
        :param image_path: str, the path of target image
        :param temp: str or ndarray, the name of template image, if ndarray, it is the image of template
        :return: ndarray, the most likely position in the image
        """

        # open the image fits file and rescale/normalize the image
        image_file = fits.open(image_path)   # open fits file
        image = (image_file[0].data).astype(self.ndtype)      # load fits data
        image_min = image.min()
        image = image - image_min * (1 - np.sign(image_min) * 0.001)    # parallel the image values
        image = self.rescaler(image)    # rescale the image
        image_min = image.min()
        image_max = image.max()
        image = (image - image_min) / (image_max - image_min) * 255 #
        img = image.copy()

        # checking the type of template and matching the image
        if isinstance(temp, str):
            template = fits.open(temp)[0].data
            res = self.matchTemplate(img, template, method=self.method)

        elif isinstance(temp, np.ndarray):

            res = self.matchTemplate(img, temp, method=self.method)

        # extract the minimum and maximum piont of residual image
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

        if self.isMax:
            return max_loc
        else:
            return min_loc

    def MulFileMatch(self, progress=True):
        """

        :param image_dir:
        :param temp_name:
        :param args:
        :param kwargs:
        :return:
        """

        temp_path = os.path.join(self.image_dir, self.temp_name)
        template = fits.open(temp_path)[0].data
        template = template.astype(self.ndtype)

        position_list = []
        file_list = os.listdir(self.image_dir)
        dir_len = len(file_list)

        if progress==True:
            for file_n in range(dir_len):
                file_name = file_list[file_n]
                if (file_name != self.temp_name):

                    file_path = os.path.join(self.image_dir, file_name)

                    position = self.MethodMatch(file_path, template)

                    position_list.append(position)

                    sys.stdout.write('\r')
                    # the exact output you're looking for:
                    sys.stdout.write("[%-1s] %d%% %d/%d" % ('='*file_n, file_n/(dir_len-1)*100, file_n, dir_len-1))
                    sys.stdout.write('\n')
                    sys.stdout.flush()
        else:
            for file_n in range(dir_len):
                file_name = file_list[file_n]
                if (file_name != self.temp_name):
                    file_path = os.path.join(self.image_dir, file_name)

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
