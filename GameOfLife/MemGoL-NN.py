import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sklearn.metrics
from time import time

import torch
import torch.nn as nn # basic building blocks for graphs
import torch.nn.functional as F # dropout, loss, activation functions, and more

# IPERPARAMETER
num_epochs = 5
learning_rate = 0.005
bechSize = 64
df = pd.read_csv("matrix_evolution_data.csv", dtype=float)
df = df.to_numpy()

# Dividi il database in training e test

x = torch.tensor(df[:, :-3], dtype= torch.float)
y = torch.tensor(df[:,-3], dtype= torch.float)
df = torch.utils.data.TensorDataset(x,y)
df_val, df_train = torch.utils.data.random_split(df, [0.2, 0.8])
dl = torch.utils.data.DataLoader(df_train, batch_size=bechSize, shuffle = True)
dl_val = torch.utils.data.DataLoader(df_val, batch_size=bechSize)

class MyStupidModel(nn.Module):
    def __init__(self):
        super(MyStupidModel, self).__init__()
        self.l0 = nn.Linear(5*3,3*3)
        self.l1 = nn.Linear(3*3, 1)

    def forward(self, x):
        x = self.l0(x)
        x = F.relu(x)
        x = self.l1(x)
        x = F.relu(x)
        return x
    

model = MyStupidModel()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)  # Move the model to the selected device

criterion = nn.L1Loss() # loss function
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
train_loss_array = []
val_loss_array = []

for epoch in range(num_epochs):
    train_running_loss = 0.0
    train_acc = 0.0
    sample_count = 0

    # Set the model to training mode: relevant for dropout, batchnorm, etc.
    model.train()
    start = time()
    ## training step
    for grids, labels in dl:
#        labels = torch.reshape(labels, (-1,1))
        ## move data to device for optimization. have to be done to work with GPU
        grids = grids.to(device)
        labels = labels.to(device)

        ## forward + backprop + loss
        evalLabels = model(grids)
        loss = criterion(evalLabels, labels)

        # Reset the gradients to zero: otherwise they accumulate!
        optimizer.zero_grad()

        # Backpropagation
        loss.backward()
        ## update model params
        optimizer.step()

        train_running_loss += loss.item()
        # classification report
        sample_count += labels.size(0)

    i = len(dl)
    train_loss_array.append(train_running_loss/i)
    model.eval()


    val_running_loss = 0 
    for grids, labels in df_val:
        grids = grids.to(device)
        labels = labels.to(device)

        ## forward + backprop + loss
        evalLabels = model(grids)
        evalLabels = evalLabels.flatten()
        loss = criterion(evalLabels, labels)

        val_running_loss += loss.item()
    val_loss_array.append(val_running_loss/len(dl_val))

    print(f"Epoch: {epoch+1} | Train: {train_running_loss / i:.4f} | Val: {val_running_loss / len(dl_val):.4f} | Time: {time()-start:.2f}")

