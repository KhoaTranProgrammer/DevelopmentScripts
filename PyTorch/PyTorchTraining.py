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

class PyTorchTraining(BaseClass):
    def __init__(self, json_data):
        BaseClass.__init__(self, json_data)

    def execute(self):
        print(f'This is execute() from {self.__class__.__name__}: {str(self.json_data)}')

        trainloader = Resource.GLOBAL_VARIABLE[self.json_data["Input"]["TrainLoader"]]
        model = Resource.GLOBAL_VARIABLE[self.json_data["Input"]["NeuralNetwork"]]
        criterion = Resource.GLOBAL_VARIABLE[self.json_data["Input"]["Criterion"]]
        optimizer = Resource.GLOBAL_VARIABLE[self.json_data["Input"]["Optimizer"]]

        testloader = Resource.GLOBAL_VARIABLE[self.json_data["Input"]["ValidationLoader"]]

        epochs = (int)(self.json_data["Input"]["Epochs"])
        steps = 0
        running_loss = 0
        print_every = 200
        train_losses, test_losses = [], []
        accuracies = []

        for epoch in range(epochs):
            for inputs, labels in trainloader:
                steps += 1
                # Move input and label tensors to the default device
                # inputs, labels = inputs.to(device), labels.to(device)
                
                logps = model.forward(inputs)
                loss = criterion(logps, labels)
                
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                running_loss += loss.item()
                
                if steps % print_every == 0:
                    test_loss = 0
                    accuracy = 0
                    model.eval()
                    with torch.no_grad():
                        for inputs, labels in testloader:
                            logps = model.forward(inputs)
                            batch_loss = criterion(logps, labels)
                            
                            test_loss += batch_loss.item()
                            
                            # Calculate accuracy
                            ps = torch.exp(logps)
                            top_p, top_class = ps.topk(1, dim=1)
                            equals = top_class == labels.view(*top_class.shape)
                            accuracy += torch.mean(equals.type(torch.FloatTensor)).item()

                    print(f"Epoch {epoch+1}/{epochs}.. "
                        f"Train loss: {running_loss/print_every:.3f}.. "
                        f"Test loss: {test_loss/len(testloader):.3f}.. "
                        f"Test accuracy: {accuracy/len(testloader):.3f}")
                    
                    train_losses.append(running_loss/print_every)
                    test_losses.append(test_loss/len(testloader))
                    accuracies.append(accuracy/len(testloader))
                    running_loss = 0
                    model.train()
