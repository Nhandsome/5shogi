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

class PolicyValueResNetwork(nn.Module):
    def __init__(self, blocks=2, channels=80, activation=nn.ReLU(), fc1=64):
        super(PolicyValueResNetwork, self).__init__()
        self.l1_1 = nn.Conv2d(in_channels=20, out_channels=channels, kernel_size=3, padding=1, stride=1, bias=False)
        self.l1_2 = nn.Conv2d(in_channels=20, out_channels=channels, kernel_size=1, stride=1, bias=False)
        self.l2 = nn.Conv2d(in_channels=20, out_channels=channels, kernel_size=1, stride=1, bias=False)
        self.bn1 = nn.BatchNorm2d(channels)
        self.act = activation

        self.block = nn.Sequential(*[ResNetBlock(channels, activation) for _ in range(blocks)])

        self.policy = nn.Conv2d(in_channels=channels, out_channels=MOVE_DIRECTION_LABEL_NUM, kernel_size=1, stride=1, bias=False)
        self.policy_bias = Bias(5*5*MOVE_DIRECTION_LABEL_NUM)

        self.value_conv1 = nn.Conv2d(in_channels=channels, out_channels=MOVE_DIRECTION_LABEL_NUM, kernel_size=1, stride=1, bias=False)
        self.value_bn = nn.BatchNorm2d(MOVE_DIRECTION_LABEL_NUM)
        self.value_fn1 = nn.Linear(5*5*MOVE_DIRECTION_LABEL_NUM, fc1)
        self.value_fn2 = nn.Linear(fc1, 1)
    
    def forward(self, x1, x2):
        out1_1 = self.l1_1(x1)
        out1_2 = self.l1_2(x1)
        out2 = self.l2(x2)
        out1 = self.bn1(out1_1 + out1_2 + out2)
        out1 = self.act(out1)

        h = self.block(out1)

        h_policy = self.policy_bias(torch.flatten(self.policy(h),1))

        h_value = self.act(self.value_bn(self.value_conv1(h)))
        h_value = self.act(self.value_fn1(torch.flatten(h_value,1)))
        h_value = self.value_fn2(h_value)
        
        return h_policy, F.sigmoid(h_value)


if __name__=='__main__':
    batch_size = 2
    test_input1 = torch.randn((batch_size, 20, 5, 5))
    test_input2 = torch.randn((batch_size, 20, 5, 5))
    print(f'TEST_INPUT SHAPE : {test_input1.shape}')
    print(f'TEST_INPUT SHAPE : {test_input2.shape}')

    test_model = PolicyValueResNetwork()

    y1, y2 = test_model(test_input1, test_input2)
    
    print(f'TEST_OUTPUT_1 SHAPE : {y1.shape}')
    print(f'TEST_OUTPUT_2 SHAPE : {y2.shape}')

    print(y2)
