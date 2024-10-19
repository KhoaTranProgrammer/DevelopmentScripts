import sys
import os
import json
import shutil
import importlib
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

        transforms_list.append(transforms.ToTensor())

        Resource.GLOBAL_VARIABLE[self.json_data["Input"]["ID"]] = transforms.Compose(
            transforms_list
        )
