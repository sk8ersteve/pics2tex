import bb

class LatexObject(object):
    def __init__(self, char, nextAtLevel, above, below):
        self.above = above
        self.below = below
        self.char = char
        self.nextAtLevel = nextAtLevel
         #list of objects, except in child case, objects are latex chars

def sup(s):
    # s is a latex string
    return '^{' + getChar(s) + '}'

def sub(s):
    # s is a latex string
    return '_{' + getChar(s) + '}'

def frac(a, b):
    return '\frac{' + getChar(a) + '}{' + getChar(b) + '}'

def generalDirection(a, b):
    # a, b bounding boxes
    # use getDirection (returns radians)
    # return string 'straightUp', 'straightDown', 'upRight', ...
    angle = a.getDirection(b)
    #adjust angle for easier comparison
    A = (angle+(45/2)) % 360
    if (A < 45):
        return "right"
    elif (A < 90):
        return "upRight"
    elif (A < 135):
        return "straightUp"
    elif (A < 270):
        return "other"
    elif (A < 315):
        return "straightDown"
    else: return "downRight"
    
def getChar(x):
    return x.char

def approximatelyEqual(sa, sb):
    frac = float(sa) / float(sb)
    return frac < 1.25 and frac > 0.8

# returns latex text and a list of what is left
def getLatex(l, prefix=''):
    # l is a list of bounding boxes
    if len(l)==0:
        return None
    if len(l) == 1:
        return getChar(l[0])

    s = [] 
    a = l.pop(0)
    ca = getChar(a)
    # Get BBs near a
    sortedRow = sorted(l, lambda b: b.minX)

    nearest = None
    nearestIndex = 0
    for i, b in enumerate(sortedRow):
        if (direction=='right') and approximatelyEqual(b.getSize(), a.getSize()):
            nearest = b
            nearestIndex = i
            break

    currentScope = sortedRow[:nearestIndex]
    nextRight = sortedRow[nearestIndex]
    remainingScope = sortedRow[nearestIndex]
    belowThresh = a.getBelowThreshold()
    aboveThresh = a.getAboveThreshold()

    if (nearest != None):
        #find nearest smaller upRight if exists

        #find nearest smaller downRight if exists

        allAbove =  filter(currentScope, lambda b: (b.getCenter()[1])>aboveThresh )
        allBelow =  filter(currentScope, lambda b: (b.getCenter()[1])<belowThresh )


        texAbove = getLatex(allAbove)
        texBelow = getLatex(allBelow)
        texRight = getLatex(remainingScope)
        return LatexObject(ca, texRight, texAbove, texBelow)
def latexObjToString(someLatexObj):
    s = ''
    if someLatexObj==None:
        return s
    s+=someLatexObj.char
    s+= '^{' + latexObjToString(someLatexObj.above) + '}'
    s+='_{' + latexObjToString(someLatexObj.below) + '}'
    s+=nextAtLevel(latexObjToString(someLatexObj.nextAtLevel))
    return s

