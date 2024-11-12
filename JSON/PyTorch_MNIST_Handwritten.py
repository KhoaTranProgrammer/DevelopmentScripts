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

class PyTorch_MNIST_Handwritten():

    def getNetwork(self):
        class Net(nn.Module):
            def __init__(self):
                super().__init__()
                self.flatten = nn.Flatten()
                self.linear_relu_stack = nn.Sequential(
                    nn.Linear(28*28, 512),
                    nn.ReLU(),
                    nn.Linear(512, 10)
                )

            def forward(self, x):
                x = self.flatten(x)
                logits = self.linear_relu_stack(x)
                return logits

        network = Net()
        return network

    def trainNetwork(self, model, trainLoader, validationLoader, criterion, optimizer, epochs):
        num_epochs = epochs
        # Establish a list for our history
        train_loss_history = list()
        val_loss_history = list()

        for epoch in range(num_epochs):
            model.train()
            train_loss = 0.0
            train_correct = 0
            for i, data in enumerate(trainLoader):
                # data is a list of [inputs, labels]
                inputs, labels = data

                optimizer.zero_grad()

                outputs = model(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()

                _, preds = torch.max(outputs.data, 1)
                train_correct += (preds == labels).type(torch.float).sum().item()
                train_loss += loss.item()
            train_correct /= len(trainLoader.dataset)
            print(f'Epoch {epoch + 1} training accuracy: {(100*train_correct):>0.1f}% training loss: {train_loss/len(trainLoader):.5f}')
            train_loss_history.append(train_loss/len(trainLoader))

            val_loss = 0.0
            val_correct = 0
            model.eval()
            with torch.no_grad():
                for inputs, labels in validationLoader:
                    outputs = model(inputs)
                    loss = criterion(outputs, labels)

                    _, preds = torch.max(outputs.data, 1)
                    val_correct += (preds == labels).type(torch.float).sum().item()
                    val_loss += loss.item()
            val_correct /= len(validationLoader.dataset)
            print(f'Epoch {epoch + 1} validation accuracy: {(100*val_correct):>0.1f}% validation loss: {val_loss/len(validationLoader):.5f}')
            val_loss_history.append(val_loss/len(validationLoader))

    def testingNetwork(selfmodel, model, testLoader, criterion):
        test_loss = 0.0
        test_correct = 0
        model.eval()

        with torch.no_grad():
            for inputs, labels in testLoader:
                
                outputs = model(inputs)
                loss = criterion(outputs, labels)

                _, preds = torch.max(outputs.data, 1)
                test_correct += (preds == labels).sum().item()
                test_loss += loss.item()
            test_correct /= len(testLoader.dataset)
            print(f'Testing accuracy: {(100 * test_correct):>0.1f}% testing loss: {test_loss/len(testLoader):.5f}')
