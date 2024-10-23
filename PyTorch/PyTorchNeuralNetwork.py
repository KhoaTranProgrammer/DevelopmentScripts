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
import sys

class PyTorchNeuralNetwork(BaseClass):
    def __init__(self, json_data):
        BaseClass.__init__(self, json_data)

    def execute(self):
        print(f'This is execute() from {self.__class__.__name__}: {str(self.json_data)}')

        # D:/Develop/DevelopmentScripts/JSON/PyTorchSampeNeuralNetwork.py
        python_defined_network = self.json_data["Input"]["DefinedNet"]
        file_name = os.path.basename(python_defined_network) # PyTorchSampeNeuralNetwork.py
        file_path = python_defined_network.split(file_name)[0] # D:/Develop/DevelopmentScripts/JSON/
        module_name = os.path.splitext(file_name)[0] # PyTorchSampeNeuralNetwork

        sys.path.append(file_path)
        module = importlib.import_module(f'{module_name}')
        my_class = getattr(module, f'{module_name}')
        my_instance = my_class()
        
        Resource.GLOBAL_VARIABLE[self.json_data["Input"]["ID"]] = my_instance.getNetwork()
