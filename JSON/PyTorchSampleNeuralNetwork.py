import sys
import os
import json
import shutil
import importlib
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np

class PyTorchSampleNeuralNetwork():

    def getNetwork(self):
        class Classifier(nn.Module):
            def __init__(self):
                super().__init__()

                self.fc1 = nn.Linear(3*32*32, 64)
                self.fc2 = nn.Linear(64, 32)
                self.fc3 = nn.Linear(32, 10)
                self.logsoftmax = nn.LogSoftmax(dim=1)

            def forward(self, x):
                x = x.view(x.shape[0], -1)
                x = F.relu(self.fc1(x))
                x = F.relu(self.fc2(x))
                x = self.logsoftmax(self.fc3(x))
                return x
            
        network = Classifier()
        return network
