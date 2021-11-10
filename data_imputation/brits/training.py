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

from Brits_model import Brits_i
from data_loader import get_loader

sys.path.append("../")
sys.path.append("../..")

device = torch.device("cuda")

def training(epoch, data, model_address):
    # TODO
    # model training
    length = len(data)
    model = Brits_i(108, 1, 0, length, device).to(device)
        #(hidden_state_dim, impute_weight, label_weight, length, device)
    
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    data_iter = get_loader('./brits_json/' + model_address + '.json', batch_size=64)
    # model_address 에 model 저장
    
    model.train()
    
    progress = tqdm(range(epoch))
    for i in progress:
        tl=0.0
        for idx, data in enumerate(data_iter):  
            data = to_var(data,device)
            ret = model.run_on_batch(data, optimizer, i)
            tl += ret["loss"]
        progress.set_description("loss: {:0.6f}".format(tl/len(data_iter)))
    
    torch.save(model, model_address)
    
    return model

def model_save(model_name, model):
    # folder가 있을 경우 하위에 생성, 이미 있는 파일은 삭제
    # folder가 없을 경우 임의로 폴더 생성 
    
    # 전체 모델 저장
    torch.save(model, model_name + 'model.pt')
    
    # 모델 객체의 state_dict 저장
    torch.save(model.state_dict(), model_name + 'model_state_dict.pt')

    torch.save({
        'model': model.state_dict(),
        'optimizer': optimizer.state_dict()
    }, model_name + 'all.tar')
    
    pass
