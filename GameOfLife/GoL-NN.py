import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from time import time

import torch
import torch.nn as nn # basic building blocks for graphs
import torch.nn.functional as F # dropout, loss, activation functions, and more

# IPERPARAMETER
num_epochs = 20
learning_rate = 0.005
bechSize = 32
df = pd.read_csv("life_Data.csv", dtype=bool)
df = df.to_numpy()

# Dividi il database in training e test
x = torch.tensor(df[:, 1:], dtype= torch.float)
y = torch.tensor(df[:,0], dtype= torch.float)
df = torch.utils.data.TensorDataset(x,y)
dl = torch.utils.data.DataLoader(df, batch_size=bechSize, shuffle = True)

class MyModel(nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()
        self.l0 = nn.Linear(3*3,3*3)
        self.l1 = nn.Linear(3*3, 1)

    def forward(self, x):
        x = self.l0(x)
        x = F.relu(x)
        x = self.l1(x)
        x = F.sigmoid(x)
        return x
    
def get_batch_accuracy(logit, target):
    """Obtain accuracy for one batch of data"""
    corrects = ((logit.data > 0.5) == target.data).sum()
    return corrects.item()



model = MyModel()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)  # Move the model to the selected device

criterion = nn.BCELoss() # loss function
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

for epoch in range(num_epochs):
    train_running_loss = 0.0
    train_acc = 0.0
    sample_count = 0

    # Set the model to training mode: relevant for dropout, batchnorm, etc.
    model.train()
    start = time()
    ## training step
    for i, (grids, labels) in enumerate(dl):
        labels = torch.reshape(labels, (-1,1))
        
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
        train_acc += get_batch_accuracy(evalLabels, labels)
        sample_count += labels.size(0)

    
    model.eval()
    print(f"Epoch: {epoch+1} | Loss: {train_running_loss / i:.4f} | Train Accuracy: {train_acc/sample_count:.4f} | Time: {time()-start:.2f}")