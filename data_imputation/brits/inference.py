import torch
import numpy as np
from Brits_model import *

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

def model_load(model_name):
    # TODO 
    # model을 로드하여 전달함
    PATH = model_name
    model = torch.load(PATH)
    return model

def evaluate(data_iter, model):
    model.eval()
    imputations = []
    for idx, data in enumerate(data_iter):
        data = to_var(data, device)
        ret = model.run_on_batch(data, None)
        eval_masks = ret['eval_masks'].data.cpu().numpy()
        imputation = ret['imputations'].data.cpu().numpy()
        imputations += imputation[np.where(eval_masks == 1)].tolist()
    imputations = np.asarray(imputations)
    return imputation

def inference(model, data_iter, device, df):
    column_name = df.columns[0]
    imputation = evaluate(model, data_iter, device)
    scaler = StandardScaler()
    scaler = scaler.fit(df[column_name].to_numpy().reshape(-1,1))
    result = scaler.inverse_transform(imputation[0])
    return result[:, 0]