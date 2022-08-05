"""
========================================================

        Introduction to artificial intelligence

                         PacNET

========================================================
@ Victor Mangeleer - S181670

-------------
Documentation
-------------

This script has for purpose to train our PacNET using
the data available in the DATA folder.

"""

# Others
import os
import glob
import time
import numpy as np

from others.display import *
from others.training import *
from others.data_model import *

# Pytorch
import torch
import torch.nn as nn
import torch.optim as optim


#----------------------------------------------------------
#
#                     Parameters of PacNET
# 
#----------------------------------------------------------
# Number of epochs
nb_epoch = 1000

# Size of the bach in the dataloader
batch_size = 64

# Learning rate of the training
learning_rate = 0.001

# Define the percentage of the complete dataset that will be used as a train set
train_size  = 80

# Define the version of your PacNET
pacnet_version = "PacNET"

# Terminal UI
PacNET_Logo()
PacNET_Usage()
if len(os.listdir('../data')) < 2:
    PacNET_Alert()
    exit()
PacNET_Training()

#----------------------------------------------------------
#
#                 Loading & preparing the data
# 
#----------------------------------------------------------
x, y = loadData("../data/x.txt", "../data/y.txt")

# Conversion to torch
x = torch.tensor(x, dtype=torch.double)
y = torch.tensor(y, dtype=torch.double)

# Creation of the train and validation sets
size_training = int(x.shape[0] * (train_size/100))

dataset_train = PM_Dataset(x[:size_training, :, :], y[:size_training, :])
dataset_valid = PM_Dataset(x[size_training:, :, :], y[size_training:, :])

PM_train = DataLoader(dataset_train, batch_size = batch_size)
PM_valid = DataLoader(dataset_valid, batch_size = batch_size)


#----------------------------------------------------------
#
#                     Training PacNET
# 
#----------------------------------------------------------
# Creation of the neural network
pacnet = PacNET().float()

# Definition of the optimizers
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(pacnet.parameters(), lr = learning_rate)

# First training information
losses_train_total = []
losses_valid_total = []

# Other parameters
t_size = len(dataset_train) + 1
v_size = len(dataset_train)
estimated_time = 0

# Going through epochs
for epoch in range(nb_epoch):

    # Used to compute the average loss value over the all epoch
    train_losses = []
    valid_losses = []

    # Display useful information
    index = batch_size
    start = time.time()

    # Display useful information
    print("\nEpoch : ", epoch + 1, "/", nb_epoch, "\n")

    #---------------------------------------------------------------------------
    #                                   Training
    #---------------------------------------------------------------------------
    for x, y in PM_train:

        # Computing SBOT prediction
        pred = pacnet(x.float())
        
        # Computing the loss
        loss = criterion(pred, y) 

        # Adding the loss
        train_losses.append(loss.detach().item())

        # Reseting the gradients
        optimizer.zero_grad()

        # Backward pass
        loss.backward()

        # Optimizing the parameters
        optimizer.step()

         # Update the progress bar
        time_left = estimated_time - (time.time() - start)
        progressBar(loss, 0, time_left, (index/t_size)*100)
        index = index + batch_size

    # Computing mean loss
    mean_loss = sum(train_losses)/len(train_losses)
    losses_train_total.append(mean_loss)

    # Display useful information
    estimated_time = time.time() - start
    progressBar(mean_loss, 0, 0, 100)

    #---------------------------------------------------------------------------
    #                                 Validation
    #---------------------------------------------------------------------------
    index_validation = batch_size

    with torch.no_grad():  
        
        for x, y in PM_valid:

            # Computing SBOT prediction
            pred = pacnet(x.float())
            
            # Computing the loss
            loss_2 = criterion(pred, y) 

            # Adding the loss
            valid_losses.append(loss_2.detach().item())

            # Update the progress bar
            progressBar(mean_loss, loss_2, time_left, (index_validation/v_size)*100)
            index_validation = index_validation + batch_size

    
    # Computing mean loss
    mean_loss_2 = sum(valid_losses)/len(valid_losses)

    # Adding the final loss of the epoch
    losses_valid_total.append(mean_loss_2)

    # Display useful information
    estimated_time = time.time() - start
    progressBar(mean_loss, mean_loss_2, 0, 100)
    print("\n")

# Saving the result
saveModel("PacNETs/", pacnet_version, pacnet, optimizer)

# Terminal UI
PacNET_Done()






