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

class PyTorchSampleTesting():

    def testingNetwork(selfmodel, model, validationLoader):
        accuracy = 0
        model.eval()
        with torch.no_grad():
            for images, labels in validationLoader:
                # images = images.to(device)
                # labels = labels.to(device)
                logps = model.forward(images)

                ps = torch.exp(logps)
                top_p, top_class = ps.topk(1, dim=1)
                equality = top_class == labels.view(*top_class.shape)
                accuracy += torch.mean(equality.type(torch.FloatTensor)).item()
        model.train()
        print(f"Test accuracy: {accuracy/len(validationLoader):.4%}")
