import bb
import algorithm

a = bb.BoundingBox(-1,1,-1,1)
b = bb.BoundingBox(0,4,0,1)
c = bb.BoundingBox(0,1,0,4)
d = bb.BoundingBox(0,2,0,2)
print(algorithm.generalDirection(a,b))
print(algorithm.generalDirection(a,c))
print(algorithm.generalDirection(a,d))
