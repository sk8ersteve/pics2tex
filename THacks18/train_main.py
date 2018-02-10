import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torch.backends.cudnn as cudnn
from torch.autograd import Variable
import torchvision
import torchvision.transforms as transforms

import os
import argparse

from vgg import VGG
from imageLoading import get_im_data

parser = argparse.ArgumentParser(description='PyTorch Math Charecter Recognition Training')
parser.add_argument('--lr', default=0.01, type=float, help='learning rate')

args = parser.parse_args()

use_cuda = torch.cuda.is_available()
print (use_cuda)
best_acc = 0  # best test accuracy
start_epoch = 0  # start from epoch 0 or last checkpoint epoch

# Data
print('==> Preparing data..')
transform_train = transforms.Compose([
    #transforms.RandomCrop(32, padding=4),
    transforms.RandomRotation(25),
    transforms.ToTensor()
])

transform_test = transforms.Compose([
    transforms.ToTensor()
])

# laoding and randomly permuting the images and labels in the same way
(imgs, labels) = get_im_data()
mixer = torch.randperm(imgs.size(0))

imgs = imgs[mixer]
labels = labels[mixer]

trainset = torch.utils.data.TensorDataset(imgs[:-10000], labels[:-10000])
trainloader = torch.utils.data.DataLoader(trainset, batch_size=100, shuffle=True, num_workers=2)

testset = torch.utils.data.TensorDataset(imgs[-10000:], labels[-10000:])
testloader = torch.utils.data.DataLoader(testset, batch_size=100, shuffle=False, num_workers=2)

# Model
print('==> Building model..')
net = VGG('VGG11')

if use_cuda:
    net.cuda()
    net = torch.nn.DataParallel(net, device_ids=range(torch.cuda.device_count()))
    cudnn.benchmark = True

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adadelta(net.parameters(), lr=0.01)

# Training
def train(epoch):
    print('\nEpoch: %d' % epoch)
    net.train()
    train_loss = 0
    correct = 0
    total = 0
    for batch_idx, (inputs, targets) in enumerate(trainloader):
        if use_cuda: inputs, targets = inputs.cuda(), targets.cuda()
        optimizer.zero_grad()
        inputs, targets = Variable(inputs), Variable(targets)
        outputs = net(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()

        train_loss += loss.data[0]
        _, predicted = torch.max(outputs.data, 1)
        total += targets.size(0)
        correct += predicted.eq(targets.data).cpu().sum()
    print ('Loss: %.5f | Acc: %.3f%% (%d/%d)'
            % (train_loss/(batch_idx+1), 100.*correct/total, correct, total))

def test(epoch):
    global best_acc
    net.eval()
    test_loss = 0
    correct = 0
    total = 0
    for batch_idx, (inputs, targets) in enumerate(testloader):
        if use_cuda: inputs, targets = inputs.cuda(), targets.cuda()
        inputs, targets = Variable(inputs, volatile=True), Variable(targets)
        outputs = net(inputs)
        loss = criterion(outputs, targets)

        test_loss += loss.data[0]
        _, predicted = torch.max(outputs.data, 1)
        total += targets.size(0)
        correct += predicted.eq(targets.data).cpu().sum()

    print ('Loss: %.5f | Acc: %.3f%% (%d/%d)'
            % (test_loss/(batch_idx+1), 100.*correct/total, correct, total))

    # Save checkpoint.
    acc = 100.*correct/total
    if acc > best_acc:
        print('Saving..')
        state = {
            'net': net.module if use_cuda else net,
            'acc': acc,
            'epoch': epoch,
        }
        torch.save(state, 'model.pt')
        best_acc = acc

test(0)
for epoch in range(200):
    train(epoch)
    test(epoch)
