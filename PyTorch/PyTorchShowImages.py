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

class PyTorchShowImages(BaseClass):
    def __init__(self, json_data):
        BaseClass.__init__(self, json_data)

    def execute(self):
        print(f'This is execute() from {self.__class__.__name__}: {str(self.json_data)}')

        dataiter = iter(Resource.GLOBAL_VARIABLE[self.json_data["Input"]["DataLoader"]])
        batch = next(dataiter)
        labels = batch[1][0:5]
        images = batch[0][0:5]
        for i in range(5):
            # print(classes[labels[i]])
        
            image = images[i].numpy()
            plt.imshow(image.T)
            if self.json_data["Input"]["DataLoader"] == True:
                plt.show()