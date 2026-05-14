print("start")
import numpy as np
import matplotlib.pyplot as plt
from pandas import read_csv
from time import time
import memGoL_models as mm
from tqdm import tqdm
import os

from sklearn.metrics import confusion_matrix
print("sklenar import")

from torch import device, load
from torch import save as torch_save
from torch.optim import Adam
from torch.cuda import is_available

import torch.nn as nn
import torch.nn.functional as F
print("torch import")
# IPERPARAMETER
num_epochs = 5
learning_rate = 0.001
bechSize = 64
df = read_csv("matrix_evolution_data.csv", dtype=float)
df = df.to_numpy()

# Dividi il database in training e test

train_dl, val_dl, test_dl = mm.dlCreator(data = df[:, :-3], label = df[:, -3], bechsize= bechSize)

model = mm.DumbModel()
device = device("cuda" if is_available() else "cpu")
model = model.to(device)  # Move the model to the selected device

criterion = nn.BCELoss() # loss function
optimizer = Adam(model.parameters(), lr=learning_rate)


train_loss_array = []
train_acc_array = []
val_loss_array = []
val_acc_array = []
conf_matrix = { "TP" : 0 , "FP" : 0 , "TN" : 0 , "FN" : 0}



model_path = "DumbModel" + ".pth"
train = True
if(model_path in os.listdir()):
    print("MODEL FOUND - ATTEMPTING TO LOAD")
    model.load_state_dict(load(model_path))
    print("MODEL LOADED, SKIPPING TRAINING")
    train = False



for epoch in range(num_epochs):
    train_running_loss = 0.0
    train_acc = 0.0
    sample_count = 0

    # Set the model to training mode: relevant for dropout, batchnorm, etc.
    model.train()
    start = time()
    ## training step
    for grids, labels in tqdm(train_dl, desc=f"Epoch {epoch+1}/{num_epochs}"):
#        labels = torch.reshape(labels, (-1,1))
        ## move data to device for optimization. have to be done to work with GPU
        grids = grids.to(device)
        labels = labels.to(device)

        ## forward + backprop + loss
        evalLabels = model(grids)
#        print(str(evalLabels.size()) + " " + str(labels.size()))
        loss = criterion(evalLabels, labels)

        # Reset the gradients to zero: otherwise they accumulate!
        optimizer.zero_grad()

        # Backpropagation
        loss.backward()
        ## update model params
        optimizer.step()

        train_running_loss += loss.item()
        train_acc += mm.BCEAccuracy(evalLabels, labels)
    

    i = len(train_dl)
    train_acc_array.append(train_acc / i)
    train_loss_array.append(train_running_loss/i)
    model.eval()


    val_running_loss = 0
    val_acc = 0
    for grids, labels in val_dl:
        grids = grids.to(device)
        labels = labels.to(device)

        ## forward + backprop + loss
        evalLabels = model(grids)
        loss = criterion(evalLabels, labels)
        labels = labels.data.cpu().numpy().ravel()
        evalLabels = evalLabels.data.cpu().numpy().ravel()
        print([evalLabels>0.5])
        print(labels)
        print(f"{type(evalLabels)}  {type(labels)}  {evalLabels.shape}  {labels.shape}")
        cm = confusion_matrix(evalLabels, labels)
        print(cm)
        val_running_loss += loss.item()
        val_acc += mm.BCEAccuracy(evalLabels, labels)

    
    i = len(val_dl)
    val_acc_array.append(val_acc / i)
    val_loss_array.append(val_running_loss/i)
    print(f"Epoch: {epoch+1} | Train: {train_running_loss / i:.4f} | Val: {val_running_loss / len(val_dl):.4f} | Time: {time()-start:.2f}")
    state = model.state_dict()
    torch_save(state, "LINEAR_MNIST.pth") #save best model yet
else:
    print("MODEL LOADED, SKIPPING TRAINING")

plt.figure()
plt.plot(train_loss_array)
plt.plot(val_loss_array)
plt.savefig("loss_plot.png")

plt.figure()
plt.plot(train_acc_array)
plt.plot(val_acc_array)
plt.savefig("acc_plot.png")