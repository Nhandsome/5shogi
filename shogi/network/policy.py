import torch
import torch.nn as nn
import torch.nn.functional as F

from shogi.common import *

class Bias(nn.Module):
    def __init__(self, shape):
        super(Bias, self).__init__()
        self.bias = nn.Parameter(torch.zeros(shape))
  
    def forward(self,x):
        return x + self.bias

class ResNetBlock(nn.Module):
    def __init__(self, channels, activation):
        super(ResNetBlock, self).__init__()
        self.conv1 = nn.Conv2d(channels, channels, kernel_size=3, padding=1, stride=1, bias=False)
        self.bn1 = nn.BatchNorm2d(channels)
        self.conv2 = nn.Conv2d(channels, channels, kernel_size=1, stride=1, bias=False)
        self.bn2 = nn.BatchNorm2d(channels)
        self.act = activation
    
    def forward(self, x):
        out = self.act(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))

        return self.act(out + x)

class PolicyNetwork(nn.Module):
    def __init__(self, blocks=1, channels=80, activation=nn.ReLU(), fc1=64):
        super(PolicyNetwork, self).__init__()
        self.l1_1 = nn.Conv2d(in_channels=40, out_channels=channels, kernel_size=3, padding=1, stride=1, bias=False)
        self.l1_2 = nn.Conv2d(in_channels=40, out_channels=channels, kernel_size=1, stride=1, bias=False)
        self.bn1 = nn.BatchNorm2d(channels)
        self.act = activation

        self.block = nn.Sequential(*[ResNetBlock(channels, activation) for _ in range(blocks)])

        self.policy = nn.Conv2d(in_channels=channels, out_channels=MOVE_DIRECTION_LABEL_NUM, kernel_size=1, stride=1, bias=False)
        self.policy_bias = Bias(5*5*MOVE_DIRECTION_LABEL_NUM)
    
    def forward(self, x):
        out1_1 = self.l1_1(x)
        out1_2 = self.l1_2(x)
        out1 = self.bn1(out1_1 + out1_2)
        out1 = self.act(out1)

        h = self.block(out1)

        h_policy = self.policy_bias(torch.flatten(self.policy(h),1))
        
        return h_policy


# if __name__=='__main__':
#     batch_size = 30
#     test_input = torch.randn((batch_size, 40, 5, 5))
#     print(f'TEST_INPUT SHAPE : {test_input.shape}')

#     test_model = PolicyNetwork()

#     y1 = test_model(test_input)
    
#     print(f'TEST_OUTPUT_1 SHAPE : {y1.shape}')

#     print(F.softmax(y1,1)[1])