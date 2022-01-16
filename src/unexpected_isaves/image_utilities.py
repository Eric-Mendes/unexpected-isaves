from math import sqrt
from typing import List, Tuple, NewType

import numpy as np
from matplotlib import cm
from PIL import Image


RGBColor = NewType("RGBColor", Tuple[int, int, int])

def fit_to_palette(image: Image, palette: List[RGBColor]) -> Image:
    """
    - Added on release 0.0.3;

    "Repaints" an image using a smaller set of colors.
    ## Parameters
    * :param image: Your image opened using the `PIL.Image` module;
    * :param palette: A list with the RGB tuples representing the colors you want to use when repainting the image.

    ## Return
    * :return: The same Image but painted with the smaller set of colors passed in the `palette` param.
    """
    def map_to_closest_color_in_set(pixel):
        euclidean_distance = lambda pxl, color: sqrt(sum([pow(p-c, 2) for p, c in zip(pxl, color)]))
        curr_color, curr_smallest_dist = palette[0], euclidean_distance(pixel, palette[0])

        for col in palette[1:]:
            print(col)
            dist = euclidean_distance(pixel, col)
            if dist < curr_smallest_dist:
                curr_smallest_dist = dist
                curr_color = col

        return curr_color[0] << 16 | curr_color[1] << 8 | curr_color[2]

    image = image.convert("RGB")
    image_as_array = np.array([[map_to_closest_color_in_set(pixel) for pixel in row] for row in np.array(image)])

    return Image.fromarray(np.uint8(cm.gist_earth(image_as_array)*255))
