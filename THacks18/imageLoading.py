import os
from os import listdir, walk
from os.path import isfile, join, abspath
import numpy as np
from PIL import Image
from torch import Tensor

def get_im_data():
    # image numpy array
    filelist = []
    mypath = './data/'
    ctr = 0
    indices = []

    for (dirpath, dirnames, filenames) in walk(mypath):
        if (dirpath == mypath):
            continue
        fullnames = []
        for file in filenames:
            fullname = dirpath + '/' + file
            fullnames.append(fullname)
            indices.append(ctr)
        filelist.extend(fullnames)
        ctr += 1
        
    all_images = np.array([np.array(Image.open(fname)) for fname in filelist])
    
    return (Tensor(all_images).unsqueeze(1), Tensor(indices).long())

