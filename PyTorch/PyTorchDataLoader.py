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

from Common.BaseClass import BaseClass
from Common import Resource

import torchvision.transforms as transforms

class PyTorchDataLoader(BaseClass):
    def __init__(self, json_data):
        BaseClass.__init__(self, json_data)

    def execute(self):
        print(f'This is execute() from {self.__class__.__name__}: {str(self.json_data)}')
        
        # print(self.json_data["Input"]["ID"])
        # print(self.json_data["Input"]["DataType"])
        # print(self.json_data["Input"]["Location"])
        # print(self.json_data["Input"]["Transforms"])

        download = True
        try:
            if self.json_data["Input"]["Download"] == False:
                download = False
        except:
            pass

        train = True
        try:
            if self.json_data["Input"]["Train"] == False:
                train = False
        except:
            pass

        batch_size = 32
        try:
            if self.json_data["Input"]["BatchSize"] != None:
                batch_size = (int)(self.json_data["Input"]["BatchSize"])
        except:
            pass

        if self.json_data["Input"]["DataType"] == "CIFAR10":
            data = torchvision.datasets.CIFAR10(self.json_data["Input"]["Location"], download=download, train=train, transform=Resource.GLOBAL_VARIABLE[self.json_data["Input"]["Transforms"]])
            Resource.GLOBAL_VARIABLE[self.json_data["Input"]["ID"]] = torch.utils.data.DataLoader(data, batch_size=batch_size, shuffle=True)
