import os
import functools
from pkg_resources import resource_filename
import cv2
import numpy as np

IMAGE_EXTENSIONS = ['.png', '.tif', '.jpg', '.jpeg']
GROUND_EXTENSIONS = ['.box']
GROUND_EXTENSIONS_DEFAULT = GROUND_EXTENSIONS[0]

import tempfile

from PIL import Image

IMAGE_SIZE = 1800
BINARY_THREHOLD = 180


def process_image_for_ocr(file_path):
    # TODO : Implement using opencv
    
    temp_filename = set_image_dpi(file_path)
    im_new = remove_noise_and_smooth(temp_filename)
    return im_new


def set_image_dpi(file_path):
    im = Image.open(file_path)
    length_x, width_y = im.size
    factor = max(1, int(IMAGE_SIZE / length_x))
    size = factor * length_x, factor * width_y
    # size = (1800, 1800)
    im_resized = im.resize(size, Image.ANTIALIAS)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    temp_filename = temp_file.name
    im_resized.save(temp_filename, dpi=(300, 300))
    return temp_filename


def image_smoothening(img):
    ret1, th1 = cv2.threshold(img, BINARY_THREHOLD, 255, cv2.THRESH_BINARY)

    ret2, th2 = cv2.threshold(th1, 50, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    blur = cv2.GaussianBlur(img, (5, 5), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return th3

def remove_noise_and_smooth(file_name):
    img = cv2.imread(file_name)

#    img = cv2.GaussianBlur(img, (5, 5), 0)
    img= cv2.bilateralFilter(img, 60, 100, 120)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    filtered = cv2.adaptiveThreshold(img.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 49, 3)


    kernel = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    img = image_smoothening(img)
    or_image = cv2.bitwise_or(img, closing)



    #img = cv2.GaussianBlur(img, (31, 31), 0)
  #  img = cv2.medianBlur(img, 33)
    ret2,img = cv2.threshold(or_image,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
     
#    img= cv2.bilateralFilter(img, 30, 100, 100)
    return img




def open_img(path_or_name):
    """
    Fuzzy finds a image file given a absolute or relative path, or a name.
    The name might have no extension, or be in the DATA_DIRECTORY
    """
    try_img_ext = functools.partial(try_extensions, IMAGE_EXTENSIONS)
    path = path_or_name
    if not os.path.exists(path):
        # proceed even when there's no result. ImageFile decides on the exception to raise
        path = try_img_ext(path_or_name) or try_img_ext(data_dir_path) or path
    return ImageFile(path)

def try_extensions(extensions, path):
    """checks if various extensions of a path exist"""
    for ext in [""] + extensions:
        if os.path.exists(path + ext):
            return path + ext
    return None


class GroundFile(object):
    """A file with ground truth data about a image (i.e.: characters and their position)"""
    def __init__(self, path):
        self.path = path
        self.segments = None
        self.classes = None

    def read(self):
        self.classes, self.segments = read_boxfile(self.path)

    def write(self):
        write_boxfile(self.path, self.classes, self.segments)


class ImageFile(object):
    """
    An OCR image file. Has an image and its file path, and optionally
    a ground (ground segments and classes) and it's file path
    """

    def __init__(self, image_path):
        if not os.path.exists(image_path):
            raise IOError("Image file not found: " + image_path)
        
        
        self.image_path = "working"+image_path
        cv2.imwrite(self.image_path, process_image_for_ocr(image_path))
        self.image = cv2.imread(self.image_path)

        basepath = os.path.splitext(self.image_path)[0]
        self.ground_path = try_extensions(GROUND_EXTENSIONS, basepath)
        if self.ground_path:
            self.ground = GroundFile(self.ground_path)
            self.ground.read()
        else:
            self.ground_path = basepath + GROUND_EXTENSIONS_DEFAULT
            self.ground = None

    @property
    def is_grounded(self):
        """checks if this file is grounded"""
        return not (self.ground is None)

    def set_ground(self, segments, classes, write_file=False):
        """creates the ground, saves it to a file"""
        if self.is_grounded:
            print("Warning: grounding already grounded file")
        self.ground = GroundFile(self.ground_path)
        self.ground.segments = segments
        self.ground.classes = classes
        if write_file:
            self.ground.write()

    def remove_ground(self, remove_file=False):
        """removes ground, optionally deleting it's file"""
        if not self.is_grounded:
            print("Warning: ungrounding ungrounded file")
        self.ground = None
        if remove_file:
            os.remove(self.ground_path)
