import sys
import os
import json
import shutil
import importlib
import numpy as np
from pathlib import Path

from Common.BaseClass import BaseClass
from Common import Resource

import torchvision.transforms as transforms

class PyTorchTransforms(BaseClass):
    def __init__(self, json_data):
        BaseClass.__init__(self, json_data)

    def execute(self):
        print(f'This is execute() from {self.__class__.__name__}: {str(self.json_data)}')

        transforms_list = []
        transforms_list.append(transforms.ToTensor())
        
        # Rotation
        try:
            if self.json_data["Input"]["Rotation"] != None:
                transforms_list.append(transforms.RandomRotation((int)(self.json_data["Input"]["Rotation"])))
        except:
            pass

        # ResizedCrop
        try:
            if self.json_data["Input"]["ResizedCrop"] != None:
                transforms_list.append(transforms.RandomResizedCrop((int)(self.json_data["Input"]["ResizedCrop"])))
        except:
            pass

        # HorizontalFlip
        try:
            if self.json_data["Input"]["HorizontalFlip"] == True:
                print("support RandomHorizontalFlip")
                transforms_list.append(transforms.RandomHorizontalFlip())
        except:
            pass

        # Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        try:
            if self.json_data["Input"]["Normalize_Mean"] != None and self.json_data["Input"]["Normalize_Std"] != None:
                list_mean = np.fromstring(self.json_data["Input"]["Normalize_Mean"], dtype=float, sep=',')
                list_std = np.fromstring(self.json_data["Input"]["Normalize_Std"], dtype=float, sep=',')
                transforms_list.append(transforms.Normalize(list_mean, list_std))
        except:
            pass

        Resource.GLOBAL_VARIABLE[self.json_data["Input"]["ID"]] = transforms.Compose(
            transforms_list
        )
