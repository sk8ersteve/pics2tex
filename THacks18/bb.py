import numpy as np

class BoundingBox(object):
    def __init__(self, minX, maxX, minY, maxY):
        self.minX = int(minX)
        self.maxX = int(maxX)
        self.minY = int(minY)
        self.maxY = int(maxY)
    
    def getCenter(self):
        centerX, centerY = (self.minX + self.maxX) / 2., (self.minY + self.maxY) / 2.
        return centerX, centerY
    def getAboveThreshold(self):
        cX,cY = self.getCenter()
        return cY + 0.1*math.abs(self.maxY-self.minY)

    def getBelowThreshold(self):
        cX,cY = self.getCenter()
        return cY - 0.1*math.abs(self.maxY-self.minY)

    def getDirection(self, other):
        x1,y1 = self.getCenter()
        x2,y2 = other.getCenter()
        ang = np.arctan2(y2-y1,x2-x1)
        return np.rad2deg((ang) % (2 * np.pi))
    
    def getDistance(self, other):
        #???? need to figure out how to reimplement without the matrix
        np.linalg.norm(self.coords-other.coords)
    
    def getSize(self):
        return (self.maxX-self.minX)*(self.maxY-self.minY)
