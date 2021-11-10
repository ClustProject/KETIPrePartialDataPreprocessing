import torch
from Brits_model import Brits_i

def model_load(model_name):
    # TODO 
    # model을 로드하여 전달함
    model = Brits_i()
    
    model = torch.load(PATH)
    return model

def inference(data, model):
    # TODO
    # model을 불러온 후 data를 imputation하고 결과를 전달
    model.eval()
    result = data
    return result