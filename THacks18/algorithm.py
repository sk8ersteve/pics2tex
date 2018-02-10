import bb

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
    return frac < 1.5 and frac > 0.66

# returns latex text and a list of what is left
def getLatex(l, inExp=False, inSub=False, prefix=''):
    # l is a list of bounding boxes
    s = ''
    
    a = l.pop(0)
    ca = getChar(a)
    # Get BBs near a
    neigbors = getNear(a, l)
    neigbors = sorted(neigbors, lambda b: dist(a,b))
    for b in neighbors:
        direction = generalDirection(a, b)
        cb = getChar(b)
        '''
        if (direction=='straightUp'):
            if ca == '-' or ca=='\Sigma':
                #lookFor straightDown frac of those 
        
        if (direction=='straightDown'):
            if ca == '-' or ca=='\Sigma':
                #lookFor straightDown frac of those
        '''

        if (direction=='upRight'):
            if inSub:
                if approximatelyEqual(a.getSize(), b.getSize()): s += cb
                elif b.getSize() > a.getSize(): return getLatex(l, prefix=prefix + sup(s))
                 #(size(b) < size(a))
                else: return getLatex(l, inExp=True, prefix=s)
            else: return getLatex(l, inExp=True, prefix=s)

        if (direction=='downRight'):
            if inExp:
                if approximatelyEqual(size(a), size(b)): s += cb
                elif size(b) > size(a): return getLatex(l, prefix=prefix + sup(s))
                #(size(b) < size(a))
                else: return getLatex(l, inSub=True, prefix=s)
            else: return getLatex(l, inSub=True, prefix=s)

        if (direction=='right'):
            return getLatex(l, prefix=s+ca)
            


