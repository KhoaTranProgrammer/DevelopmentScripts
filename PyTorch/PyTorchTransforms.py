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
        self._randomRotation = 30
        self._randomResizedCrop = 32

    def execute(self):
        print(f'This is execute() from {self.__class__.__name__}: {str(self.json_data)}')

        print(self.json_data["Input"]["Rotation"])
        print(self.json_data["Input"]["ResizedCrop"])
        print(self.json_data["Input"]["HorizontalFlip"])

        Resource.GLOBAL_VARIABLE[self.json_data["Input"]["ID"]] = transforms.Compose([
            transforms.RandomRotation(30),
            transforms.RandomResizedCrop(32),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor()
        ])

        test_transform = transforms.Compose([
            transforms.ToTensor()
        ])

        # script_dir = Path(os.path.dirname(os.path.abspath(__file__))).as_posix()
        # if os.path.exists(os.path.join(script_dir, self.json_data["Input"]["Type"] + ".py")):
        #     print(f'[TESTTYPE] {self.json_data["Input"]["Type"]} is supported')
        #     stage = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
        #     module = importlib.import_module(f'{stage}.{self.json_data["Input"]["Type"]}')
        #     my_class = getattr(module, f'{self.json_data["Input"]["Type"]}')
        #     my_instance = my_class(self.json_data)
        #     my_instance.execute()
        # else:
        #     print(f'[TESTTYPE] {self.json_data["Input"]["Type"]} is NOT supported')
