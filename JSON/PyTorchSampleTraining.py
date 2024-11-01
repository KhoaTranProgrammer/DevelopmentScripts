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

class PyTorchSampleTraining():

    def trainNetwork(self, model, trainLoader, validationLoader, criterion, optimizer, epochs):
        steps = 0
        running_loss = 0
        print_every = 200
        train_losses, test_losses = [], []
        accuracies = []

        for epoch in range(epochs):
            for inputs, labels in trainLoader:
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
                        for inputs, labels in validationLoader:
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
                        f"Test loss: {test_loss/len(validationLoader):.3f}.. "
                        f"Test accuracy: {accuracy/len(validationLoader):.3f}")

                    train_losses.append(running_loss/print_every)
                    test_losses.append(test_loss/len(validationLoader))
                    accuracies.append(accuracy/len(validationLoader))
                    running_loss = 0
                    model.train()
