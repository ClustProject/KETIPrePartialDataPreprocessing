import sys
import os
import torch
import torch.optim as optim
from torch.autograd import Variable
from torch import nn
from torch.utils.data import Dataset, DataLoader
from torch.nn.parameter import Parameter
import torch.nn.functional as F

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

from tqdm import tqdm
import ujson as json
import math

sys.path.append("../")
sys.path.append("../..")

import Brits_model

device = torch.device("cuda")

def training(data, model_address):
    # TODO
    # model training
    epoch = 100
    learning_rate = 0.01

    # setting
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    torch.random.manual_seed(0)
    np.random.seed(0)

    length = len(data)
    model = Brits_model.Brits_i(108, 1, 0, length, device).to(device)
    # Brits_model.Brits_i(hidden_state_dim, impute_weight, label_weight, length, device)
    Brits_model.makedata(data)
    
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    # data.json 파일 불러오기
    data_iter = Brits_model.get_loader('./data_imputation/brits/brits_json/data.json', batch_size=64)  

    model.train()
    
    progress = tqdm(range(epoch))
    loss_graphic = []
    for i in progress:
        total_loss = 0.0
        for idx, data in enumerate(data_iter):
            data = Brits_model.to_var(data, device)
            ret = model.run_on_batch(data, optimizer, i)
            total_loss += ret["loss"]
        loss_graphic.append(total_loss.tolist())
        progress.set_description("loss: {:0.4f}".format(total_loss / len(data_iter)))

    torch.save(model, model_address + 'model.pt')

    return model