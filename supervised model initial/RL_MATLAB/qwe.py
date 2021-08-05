import numpy as np
import torch
from torch.utils.data import TensorDataset, DataLoader
import time
import matplotlib.pyplot as plt

import sys
import itertools
import numpy as np

import torch
from torch.utils.data import TensorDataset, DataLoader

import anfis
from membership import TrapezoidalMembFunc, make_trap_mfs, make_bell_mfs, BellMembFunc, Zero, make_zero
from experimental import train_anfis, test_anfis

def abc(a,b,c):
    model = torch.load('anfis_model.npy')
    x = torch.tensor([[a,b,c]])
    x = model(x).item()
    print(type(x))
    return x
