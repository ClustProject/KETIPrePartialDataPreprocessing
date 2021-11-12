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
from data_loader import get_loader

device = torch.device("cuda")

# def to_var(var, device):
#     if torch.is_tensor(var):
#         var = Variable(var)
#         # if torch.cuda.is_available():
#         var = var.to(device)
#         return var
#     if isinstance(var, int) or isinstance(var, float) or isinstance(var, str):
#         return var
#     if isinstance(var, dict):
#         for key in var:
#             var[key] = to_var(var[key], device)
#         return var
#     if isinstance(var, list):
#         var = map(lambda x: to_var(x, device), var)
#         return var


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
        #(hidden_state_dim, impute_weight, label_weight, length, device)
    Brits_model.makedata(data)
    
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    data_iter = get_loader('./brits_json/' + model_address + '.json', batch_size=64)
    # model_address 에 model 저장
    
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




# def model_save(model_name, model):
#     # folder가 있을 경우 하위에 생성, 이미 있는 파일은 삭제
#     # folder가 없을 경우 임의로 폴더 생성 
    
#     # 전체 모델 저장
#     torch.save(model, model_name + 'model.pt')
    
#     # 모델 객체의 state_dict 저장
#     torch.save(model.state_dict(), model_name + 'model_state_dict.pt')

#     torch.save({
#         'model': model.state_dict(),
#         'optimizer': optimizer.state_dict()
#     }, model_name + 'all.tar')
    
#     pass
