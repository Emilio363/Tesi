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

from torch import device, load, no_grad
from torch import save as torch_save
from torch.cuda import is_available

import torch.nn as nn
import torch.nn.functional as F
print("torch import")

# IPERPARAMETER
num_epochs = 50
learning_rate = 0.001
bechSize = 64
df = read_csv("matrix_evolution_data.csv", dtype=float)
df = df.to_numpy()

train_dl, val_dl, test_dl = mm.dlCreator(data = df[:, :-3], label = df[:, -3], bechsize = bechSize)

val_loss_array = []
val_acc_array = []
conf_matrix = { "TP" : 0 , "FP" : 0 , "TN" : 0 , "FN" : 0}

device = device("cuda" if is_available() else "cpu")
loss = nn.BCELoss()

model = mm.DumbModel(loss, learning_rate).to(device)
model_path = "DumbModel" + ".pth"
train = True
if(model_path in os.listdir()):
    model.load_state_dict(load(model_path))
    print("Model found and skipping training")
    train = False
else:
    train_loss_array, train_acc_array = model.training_routine(train_dl, num_epochs)
    status = model.state_dict()
    torch_save(status, model_path)



with no_grad():
    val_running_loss = 0
    val_acc = 0
    for grids, labels in val_dl:
        grids = grids.to(device)
        labels = labels.to(device)

        ## forward + backprop + loss
        evalLabels = model(grids)
        loss = model.loss(evalLabels, labels)
        labels = labels.data.cpu().numpy().ravel()
        evalLabels = evalLabels.data.cpu().numpy().ravel()
        print([evalLabels>0.5])
        print(labels)
        print(f"{type(evalLabels)}  {type(labels)}  {evalLabels.shape}  {labels.shape}")
        cm = confusion_matrix(evalLabels, labels)
        print(cm)
        val_running_loss += loss.item()
        val_acc += mm.BCEAccuracy(evalLabels, labels)

    
# i = len(val_dl)
# val_acc_array.append(val_acc / i)
# val_loss_array.append(val_running_loss/i)



plt.figure()
plt.plot(train_loss_array)
plt.plot(val_loss_array)
plt.savefig("loss_plot.png")

plt.figure()
plt.plot(train_acc_array)
plt.plot(val_acc_array)
plt.savefig("acc_plot.png")