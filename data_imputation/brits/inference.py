import torch
import numpy as np
from Brits_model import *


def model_load(model_name):
    # TODO 
    # model을 로드하여 전달함
    PATH = model_name
    model = torch.load(PATH)
    return model

def inference(data, model):
    # TODO
    # model을 불러온 후 data를 imputation하고 결과를 전달

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
