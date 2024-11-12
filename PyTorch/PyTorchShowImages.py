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

        count = (int)(self.json_data["Input"]["Count"])
        dataiter = iter(Resource.GLOBAL_VARIABLE[self.json_data["Input"]["DataLoader"]])
        batch = next(dataiter)
        labels = batch[1][0:count]
        images = batch[0][0:count]
        for i in range(count):
            image = images[i].numpy()
            plt.title(self.json_data["Input"]["Classes"][labels[i]])
            if self.json_data["Input"]["Squeeze"] == True:
                plt.imshow(image.T.squeeze().T)
            else:
                plt.imshow(image.T)
            if self.json_data["Input"]["Show"] == True:
                plt.show()
