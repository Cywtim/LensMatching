import numpy as np
from cv2 import matchTemplate, TM_CCOEFF_NORMED
from astropy.io import fits


class FindLensTemplate():
    """
    This class is a quick method to find lens template in other waveband fits files.
    """

    def __int__(self, target_path):
        """
        :param target_path: The directory saves the lens fits files
        :return:
        """

        self.image_path_list = target_path

    def MethodMathch(self, image_path, temp, method=TM_CCOEFF_NORMED, isMax=True):
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
            res = matchTemplate(img, temp, method=method)

        elif isinstance(temp, np.ndarray):

            res = matchTemplate(img, temp, method=method)

        min_val, max_val, min_loc, max_loc = minMaxLoc(res)

        if isMax:
            return max_loc
        else:
            return min_loc

    def MulFileMatch(self, image_list_path):

        for file_path in

        return 0

    def MulMethodMatch(self, image, temp, methods=None, isMax=True):

        if methods is None:
            methods = [TM_CCOEFF_NORMED]

        res_ms = []

        img = image.copy()

        for method in methods:
            res_m = matchTemplate(img, temp, method=method)

            res_ms.append(res_m)

        res_ms = np.array(res_ms)

        min_val, max_val, min_loc, max_loc = minMaxLoc(res_ms)

        if isMax:
            return max_loc
        else:
            return min_loc
