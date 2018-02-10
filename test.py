import sys
import cv2
import numpy as np
print ('Hello ')
#print (sys.argv[1])
#F = open(sys.argv[1], 'r')
#print (F.read())
img = cv2.imread(sys.argv[1])
for x in range (1, 100):
	print (str(x) + " " + str(img[x,x]))