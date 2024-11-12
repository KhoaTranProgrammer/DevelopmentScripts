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

class PyTorchSampleNNWithCrossEntropyLoss():

    def getNetwork(self):
        class Net(nn.Module):
            def __init__(self):
                super().__init__()
                self.activation = F.relu
                self.fc1 = nn.Linear(32 * 32 * 3, 120)
                self.fc2 = nn.Linear(120, 84)
                self.fc3 = nn.Linear(84, 10)

            def forward(self, x):
                x = torch.flatten(x, 1) # flatten all dimensions except batch
                x = self.activation(self.fc1(x))
                x = self.activation(self.fc2(x))
                x = self.fc3(x)
                return x

        network = Net()
        return network

    def trainNetwork(self, model, trainLoader, validationLoader, criterion, optimizer, epochs):
        # Establish a list for our history
        train_loss_history = list()
        val_loss_history = list()

        for epoch in range(epochs):
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
                train_correct += (preds == labels).sum().item()
                train_loss += loss.item()

            print(f'Epoch {epoch + 1} training accuracy: {train_correct/len(trainLoader):.2f}% training loss: {train_loss/len(trainLoader):.5f}')
            train_loss_history.append(train_loss/len(trainLoader))

            val_loss = 0.0
            val_correct = 0
            model.eval()
            for inputs, labels in validationLoader:

                outputs = model(inputs)
                loss = criterion(outputs, labels)

                _, preds = torch.max(outputs.data, 1)
                val_correct += (preds == labels).sum().item()
                val_loss += loss.item()
            print(f'Epoch {epoch + 1} validation accuracy: {val_correct/len(validationLoader):.2f}% validation loss: {val_loss/len(validationLoader):.5f}')
            val_loss_history.append(val_loss/len(validationLoader))

    def testingNetwork(selfmodel, model, validationLoader):
        accuracy = 0
        print(f"Test accuracy: {accuracy:.4%}")
