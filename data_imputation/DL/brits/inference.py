import torch
import os
# import Brits_model ?????
import copy 
import numpy as np
from sklearn.preprocessing import StandardScaler
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
class BritsInference():
    def __init__(self, data, parameter):
        self.inputData = data
        self.model_path = parameter['mode_address'][0]
        self.json_path = parameter['mode_address'][1]
        self.get_model()

    def get_model(self):
        if os.path.isfile(self.model_path):
            print(self.model_path)
            print(self.json_path)
        else:
            print("no_file")

    def get_result(self):
        """
        loaded_model = Brits_model.Brits_i(108, 1, 0, len(self.data), device).to(device)
        loaded_model.load_state_dict(copy.deepcopy(torch.load(self.model_path, device)))
        
        data_iter = Brits_model.get_loader(self.json_path, batch_size=64)
        result = predict_result(loaded_model, data_iter, device, self.data)
        to_csv_data = result.tolist()
        nan_data = test_data[column_name].isnull()
        ????
        """
        return self.inputData

## 아래는 클래스에 흡수시켜야 함

def model_load(model_name):
    # TODO 
    # model을 로드하여 전달함
    PATH = model_name
    model = torch.load(PATH)
    return model

def evaluate(model, data_iter, device=torch.device("cpu")):
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

def predict_result(model, data_iter, device, df):
    column_name = df.columns[0]
    imputation = evaluate(model, data_iter, device)
    scaler = StandardScaler()
    scaler = scaler.fit(df[column_name].to_numpy().reshape(-1,1))
    result = scaler.inverse_transform(imputation[0])
    return result[:, 0]

def to_var(var, device):
    if torch.is_tensor(var):
        var = var.to(device)
        return var

    if isinstance(var, int) or isinstance(var, float) or isinstance(var, str):
        return var

    if isinstance(var, dict):
        for key in var:
            var[key] = to_var(var[key], device)
        return var

    if isinstance(var, list):
        var = map(lambda x: to_var(x, device), var)
        return var
      