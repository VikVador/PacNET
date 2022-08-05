"""
========================================================

        Introduction to artificial intelligence

                         PacNET

========================================================
@ Victor Mangeleer - S181670

-------------
Documentation
-------------

This file contains functions used to display information
during the training of the PacNET. In addition to that, it
contains functions used to save & load our model.

"""

# Pytorch
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

#import torchvision
from torch.utils.data import Dataset
from torch.utils.data import DataLoader

#----------------------
# Definition of dataset
#----------------------
class PM_Dataset(Dataset):

  def __init__(self, x, y,):
      self.x = x
      self.y = y
      
  def __getitem__(self, index):
      return (self.x[index, :, :], self.y[index, :])
  
  def __len__(self):
      return self.x.shape[0]

#-------------------------
# Definition of the PacNET
#-------------------------
class PacNET(nn.Module):

    def __init__(self):
        super().__init__()

        # Layer - 1
        self.conv_1 = nn.Conv2d(in_channels = 1, out_channels = 32, padding = 1, kernel_size = (3,3))
        self.pool_1 = nn.MaxPool2d(2, 2)

        # Layer - 2
        self.conv_2 = nn.Conv2d(in_channels = 32, out_channels = 64, kernel_size = (3,3))
        self.pool_2 = nn.MaxPool2d(2, 2)

        # Fully connected layers
        self.fc1 = nn.Linear(256, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 4)

    def forward(self, x):
        
        # [N, H, W] -> [N, C, H, W]
        x = torch.unsqueeze(x, dim=1)

        x = self.pool_1(F.relu(self.conv_1(x)))
        x = self.pool_2(F.relu(self.conv_2(x)))
        x = torch.flatten(x, 1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = torch.softmax(self.fc3(x), dim=1)
        return x

#----------
# Functions
#----------
# Allow the user to load its version of PacNET
def loadModel(path, name):

    # Loading the corresponding checkpoint
    checkpoint = torch.load(path + name + ".pth")

    # Transfering the parameters
    model = PacNET()
    model.load_state_dict(checkpoint['state_dict'])

    return model


# Allow the user to save PacNET after its training
def saveModel(path, name, model, optimizer):

    # Creation of the model's name
    model_name   = path + name + ".pth"

    # Saves all the state information
    checkpoint = {
    'state_dict': model.state_dict(),
    'optimizer' : optimizer.state_dict()
    }

    # Saving everything everything
    torch.save(checkpoint, model_name)


# Convert the prediction made by PacNET into a readable move
def getMove(proba_move):

    # Retreives the index of the predicted move
    index_m = torch.argmax(proba_move)

    if index_m == 0:
        return ["North"]
    if index_m == 1:
        return ["South"]
    if index_m == 2:
        return ["East"]
    if index_m == 3:
        return ["West"]


# Display a nice looking progression bar during the training of a model
def progressBar(loss_training, loss_validation, estimated_time, percent, width = 40):

    # Setting up the useful information
    left  = width * percent // 100
    right = width - left
    tags = "#" * int(left)
    spaces = " " * int(right)
    percents = f"{percent:.2f} %"
    loss_training = f"{loss_training * 1:.6f}"
    loss_validation = f"{loss_validation * 1:.6f}"
    estimated_time = f"{estimated_time:.2f} s"

    # Displaying a really cool progress bar !
    print("\r[", tags, spaces, "] - ", percents, " | Loss (Training) = ", loss_training, " | Loss (Validation) = ", 
          loss_validation,  " | Time left : ", estimated_time ,sep="", end="", flush = True)







