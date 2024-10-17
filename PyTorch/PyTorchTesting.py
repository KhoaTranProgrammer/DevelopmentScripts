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
        test_transform = transforms.Compose([
            transforms.ToTensor()
        ])
        test_data = torchvision.datasets.CIFAR10('CIFAR10/', download=True, train=False, transform=test_transform)
        testloader = torch.utils.data.DataLoader(test_data, batch_size=32)

        accuracy = 0
        model.eval()
        with torch.no_grad():
            for images, labels in testloader:
                # images = images.to(device)
                # labels = labels.to(device)
                logps = model.forward(images)

                ps = torch.exp(logps)
                top_p, top_class = ps.topk(1, dim=1)
                equality = top_class == labels.view(*top_class.shape)
                accuracy += torch.mean(equality.type(torch.FloatTensor)).item()
        model.train()
        print(f"Test accuracy: {accuracy/len(testloader):.4%}")
