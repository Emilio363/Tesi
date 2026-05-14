import sklearn
from time import time
from tqdm import tqdm
from numpy import ndarray

from torch import tensor, float32, sigmoid, device
from torch.utils.data import TensorDataset, DataLoader
from torch.nn import Module, Linear, Conv1d
from torch.nn.functional import relu
from torch.optim import Adam

def BCEAccuracy(logit, target):
    corrects = ((logit.data > 0.5) == target.data).sum() / len(logit.data)
    return corrects.item()

def dlCreator(data : ndarray, label : ndarray, bechsize : int) -> tuple[DataLoader, DataLoader, DataLoader] :

    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(data, label, test_size = 0.2, train_size = 0.8)
    x_train, x_val, y_train, y_val = sklearn.model_selection.train_test_split(x_train, y_train, test_size = 0.2, train_size = 0.8)


    X_train_tensor = tensor(x_train, dtype=float32)
    y_train_tensor = tensor(y_train, dtype=float32)

    X_val_tensor = tensor(x_val, dtype=float32)
    y_val_tensor = tensor(y_val, dtype=float32)

    X_test_tensor = tensor(x_test, dtype=float32)
    y_test_tensor = tensor(y_test, dtype=float32)

    X_train_tensor = X_train_tensor.unsqueeze(1)
    X_val_tensor = X_val_tensor.unsqueeze(1)
    X_test_tensor = X_test_tensor.unsqueeze(1)

    train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
    val_dataset = TensorDataset(X_val_tensor, y_val_tensor)
    test_dataset = TensorDataset(X_test_tensor, y_test_tensor)

    train_dl = DataLoader(train_dataset, batch_size=bechsize, shuffle=True)
    val_dl = DataLoader(val_dataset, batch_size=bechsize, shuffle=True)
    test_dl = DataLoader(test_dataset, batch_size=bechsize, shuffle=False)

    return train_dl, val_dl, test_dl

# stupid, dumb dense slow clueless average mid smart clever bright intelligent gifted brilliant genius

class StupidModel(Module):
    def __init__(self):
        super(StupidModel, self).__init__()
        self.l0 = Linear(5*3,3*3)
        self.l1 = Linear(3*3, 1)

    def forward(self, x):
        x = self.l0(x)
        x = relu(x)
        x = self.l1(x)
        x = sigmoid(x)
        return x.flatten()

class DumbModel(Module):
    def __init__(self, loss, optimizer = Adam):
        super(DumbModel, self).__init__()
        self.loss = loss
        self.optimizer = optimizer
        self.l0 = Conv1d(in_channels = 1, out_channels=24, kernel_size=3 )
        self.l1 = Linear(24*13,6*13)
        self.l2 = Linear(6*13, 3*3)
        self.l3 = Linear(3*3, 1)

    def forward(self, x):
        x = self.l0(x)
        x = relu(x)
        x = x.flatten(1)
        x = self.l1(x)
        x = relu(x)
        x = self.l2(x)
        x = relu(x)
        x = self.l3(x)
        x = sigmoid(x) 
        return x.flatten()
    
    def training(self, train_dl : DataLoader, max_epochs : int, loss = None, optimizer = None) -> Module:
        loss = loss if loss != None else self.loss
        optimizer = optimizer if optimizer != None else self.optimizer
        train_acc_array = []
        train_loss_array = []
        for epoch in range(max_epochs):
            train_running_loss = 0.0
            train_acc = 0.0
            sample_count = 0

            self.train()
            start = time()

            for grids, labels in tqdm(train_dl, desc=f"Epoch {epoch+1}/{max_epochs}"):
                grids = grids.to(device)
                labels = labels.to(device)

                evalLabels = self(grids)
                loss = loss(evalLabels, labels)

                optimizer.zero_grad()

                loss.backward()
                optimizer.step()

                train_running_loss += loss.item()
                train_acc += BCEAccuracy(evalLabels, labels)
            

            i = len(train_dl)
            train_acc_array.append(train_acc / i)
            train_loss_array.append(train_running_loss/i)
            self.eval()
        
            print(f"Epoch: {epoch+1} | Train: {train_running_loss / i:.4f} | Time: {time()-start:.2f}")
            state = self.state_dict()
    
        return state, train_loss_array, train_acc_array