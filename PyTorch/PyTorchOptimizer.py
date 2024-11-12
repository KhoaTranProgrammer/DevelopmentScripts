import sys
import os
import json
import shutil
import importlib
from pathlib import Path

from Common.BaseClass import BaseClass
from Common import Resource

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np

class PyTorchOptimizer(BaseClass):
    def __init__(self, json_data):
        BaseClass.__init__(self, json_data)

    def execute(self):
        print(f'This is execute() from {self.__class__.__name__}: {str(self.json_data)}')

        if self.json_data["Input"]["Optim"] == "SGD":
            lr = (float)(self.json_data["Input"]["LR"])
            momentum = 0.0
            try:
                if self.json_data["Input"]["Momentum"] != None:
                    momentum = (float)(self.json_data["Input"]["Momentum"])
            except:
                pass
            
            Resource.GLOBAL_VARIABLE[self.json_data["Input"]["ID"]] = optim.SGD((Resource.GLOBAL_VARIABLE[self.json_data["Input"]["NeuralNetwork"]]).parameters(), lr=lr, momentum=momentum)
        elif self.json_data["Input"]["Optim"] == "Adam":
            lr = (float)(self.json_data["Input"]["LR"])
            Resource.GLOBAL_VARIABLE[self.json_data["Input"]["ID"]] = optim.Adam((Resource.GLOBAL_VARIABLE[self.json_data["Input"]["NeuralNetwork"]]).parameters(), lr=lr)
