import sklearn
import torch
import torch.nn as nn
import torch.nn.functional as F

def BCEAccuracy(logit, target):
    corrects = ((logit.data > 0.5) == target.data).sum()
    return corrects.item()

def dlCreator(data, label, bechsize):

    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(data, label, test_size = 0.2, train_size = 0.8)
    x_train, x_val, y_train, y_val = sklearn.model_selection.train_test_split(x_train, y_train, test_size = 0.2, train_size = 0.8)


    X_train_tensor = torch.tensor(x_train, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train, dtype=torch.float32)

    X_val_tensor = torch.tensor(x_val, dtype=torch.float32)
    y_val_tensor = torch.tensor(y_val, dtype=torch.float32)

    X_test_tensor = torch.tensor(x_test, dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test, dtype=torch.float32)

    X_train_tensor = X_train_tensor.unsqueeze(1)
    X_val_tensor = X_val_tensor.unsqueeze(1)
    X_test_tensor = X_test_tensor.unsqueeze(1)

    train_dataset = torch.utils.data.TensorDataset(X_train_tensor, y_train_tensor)
    val_dataset = torch.utils.data.TensorDataset(X_val_tensor, y_val_tensor)
    test_dataset = torch.utils.data.TensorDataset(X_test_tensor, y_test_tensor)

    train_dl = torch.utils.data.DataLoader(train_dataset, batch_size=bechsize, shuffle=True)
    val_dl = torch.utils.data.DataLoader(val_dataset, batch_size=bechsize, shuffle=True)
    test_dl = torch.utils.data.DataLoader(test_dataset, batch_size=bechsize, shuffle=False)

    return train_dl, val_dl, test_dl

# stupid, dumb dense slow clueless average mid smart clever bright intelligent gifted brilliant genius

class StupidModel(nn.Module):
    def __init__(self):
        super(StupidModel, self).__init__()
        self.l0 = nn.Linear(5*3,3*3)
        self.l1 = nn.Linear(3*3, 1)

    def forward(self, x):
        x = self.l0(x)
        x = F.relu(x)
        x = self.l1(x)
        x = F.sigmoid(x)
        return x.flatten()

class DumbModel(nn.Module):
    def __init__(self):
        super(DumbModel, self).__init__()
        self.l0 = nn.Conv1d(in_channels = 1, out_channels=24, kernel_size=3 )
        self.l1 = nn.Linear(24*13,6*13)
        self.l2 = nn.Linear(6*13, 3*3)
        self.l3 = nn.Linear(3*3, 1)

    def forward(self, x):
        x = self.l0(x)
        x = F.relu(x)
        x = x.flatten(1)
        x = self.l1(x)
        x = F.relu(x)
        x = self.l2(x)
        x = F.relu(x)
        x = self.l3(x)
        x = torch.sigmoid(x) 
        return x.flatten()
    
