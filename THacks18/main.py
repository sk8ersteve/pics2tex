import os
import argparse
import torch
import torch.nn as nn
import json
import grounding
from algorithm import getLatex
from torch.autograd import Variable
import cv2 as cv

head = r'''
\documentclass[11pt]{article}
\usepackage{url,amsmath,setspace,amssymb,fullpage, scrextend, enumitem, enumerate, amsthm, xfrac}
\begin{document}
'''

foot = '''
\end{document}
'''

labels2Tex = ['!', '(', ')', '+', ',', '-', '\\{', '\\}', '[', ']', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '=', '[', ']', 'A', '\\alpha', '|', 'b', '\\beta', 'C', 'cos', 'd', '\\nabla', '\\div', 'e', '\\exists', 'f', '\\forall', '/', 'G', '\\gamma', '\\geq', '>', 'H', 'I', '\\in', '\\infty', '\\int', 'j', 'k', 'l', '\\lambda', '\\leq', 'log', '\\lt', 'M', '\\mu', 'N', '\\neq', 'o', 'p', '\\phi', '\\Pi', '\\pm', '`', 'q', 'R', '\\rightarrow', 'S', '\\sigma', 'sin', '\\sqrt{', '\\Sigma', 'T', 'tan', '\\theta', '\\bullet', 'u', 'v', 'W', 'X', 'y', 'z']

pad = nn.ZeroPad2d(2)

def getBody(imgFile):
    bbs, imgs = grounding.segment(imgFile)
    # Need to get imgs as a tensor
    out = [] 
    for img in imgs:
        height, width = img.size(0), img.size(1)
        img = img.numpy()
        img = cv.resize(img, (45, 45), interpolation = cv.INTER_AREA)
        img = torch.Tensor(img)
        input = Variable(img.unsqueeze(0).unsqueeze(0).cuda())
        out.append(model(input))

    out = torch.cat(out, dim=0)
    labels = torch.max(out, dim=1)[1]
    for i, l in enumerate(list(labels)):
        bbs[i].char = labels2Tex[l.data[0]]

    return getLatex(bbs)

if __name__ == '__main__':
    '''
    parser = argparse.ArgumentParser(description='Handwritting to latex')
    parser.add_argument('--imgFile', type=string, default='target.png', metavar='N',
                                help='File containing your image.')
    args = parser.parse_args()
    '''

    global model
    model = torch.load('model.pt')['net'].cuda()

    name = "out0.txt"
    i = 1
    while os.path.isfile(name):
        name = "out"+str(i)+".txt"
        i += 1
    
    f = open(name,"w+")

    body = getBody('target.png')#args.imgFile)

    f.write(head+body+foot)
    f.close()
    print ("Successfuly create .tex file!")
