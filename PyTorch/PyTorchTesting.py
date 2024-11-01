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

class PyTorchTesting(BaseClass):
    def __init__(self, json_data):
        BaseClass.__init__(self, json_data)

    def execute(self):
        print(f'This is execute() from {self.__class__.__name__}: {str(self.json_data)}')

        model = Resource.GLOBAL_VARIABLE[self.json_data["Input"]["NeuralNetwork"]]
        validationLoader = Resource.GLOBAL_VARIABLE[self.json_data["Input"]["TestLoader"]]

        # D:/Develop/DevelopmentScripts/JSON/PyTorchSampleTesting.py
        python_defined_networktraining = self.json_data["Input"]["DefinedTestingNet"]
        file_name = os.path.basename(python_defined_networktraining) # PyTorchSampleTesting.py
        file_path = python_defined_networktraining.split(file_name)[0] # D:/Develop/DevelopmentScripts/JSON/
        module_name = os.path.splitext(file_name)[0] # PyTorchSampleTesting

        sys.path.append(file_path)
        module = importlib.import_module(f'{module_name}')
        my_class = getattr(module, f'{module_name}')
        my_instance = my_class()
        
        my_instance.testingNetwork(model, validationLoader)
