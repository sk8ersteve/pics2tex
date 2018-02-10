import cv2
import numpy as np
from matplotlib import pyplot as plt
from skimage.measure import label
import copy

from files import *
from bb import BoundingBox 
from collections import defaultdict
from torch import Tensor

def segment(path='target.png'):
    image = process_image_for_ocr(path)
    ni = -1*image+255

    cp = label(ni)
    labelNum = np.amax(cp)
    #cv2.imwrite("foo.png", cp) 
    #we have the maxX, minX, maxY and minY of each BB

    N = cp.shape[0]
    M = cp[0].shape[0]
    
    bbs = []
    imgs = []

    for k in range(labelNum + 1):
        m = np.multiply(np.where(cp==k, 1, 0), ni)
        
        if (np.sum(m)>40):
            #cv2.imwrite("img"+str(k)+".png", m)
            for i in range(N):
                # Iterate until a non-zero row
                mini = i
                if (m[i].any()): break

            for i in range(N):
                # Iterate from end until a non-zero row
                maxi = len(m) - 1 - i
                if (m[-i].any()): break

            for j in range(M):
                # Iterate until a non-zero column
                minj = j
                if (m[:,j].any()): break

            for j in range(M):
                # Iterate from end until a non-zero column
                maxj = len(m[0]) - 1 - j
                if (m[:,-j].any()): break

            if (m.any()):
                bb=BoundingBox(mini, maxi, minj, maxj)
                bbs.append(bb)
                imgs.append(Tensor(image[bb.minX:bb.maxX, bb.minY:bb.maxY]))

    return bbs, imgs
