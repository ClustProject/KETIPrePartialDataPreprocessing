import torch
import os
from KETIPrePartialDataPreprocessing.data_imputation.DL.brits import Brits_model
import copy 
import numpy as np
from sklearn.preprocessing import StandardScaler
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
class BritsInference():
    def __init__(self, data, model_folder):
        self.inputData = data
        self.model_path = os.path.join(model_folder, 'in_temp.pth')
        self.json_path = os.path.join(model_folder, 'in_temp.json')
 

    def get_result(self):
        loaded_model = Brits_model.Brits_i(108, 1, 0, len(self.inputData), device).to(device)
        loaded_model.load_state_dict(copy.deepcopy(torch.load(self.model_path, device)))
        
        Brits_model.makedata(self.inputData, self.json_path)
        data_iter = Brits_model.get_loader(self.json_path, batch_size=64)
        
        result = self.predict_result(loaded_model, data_iter, device, self.inputData)
        
        to_csv_data = result.tolist()
        nan_data = self.inputData[self.inputData.columns[0]].isnull()
        for i in range(len(nan_data)):
            if nan_data.iloc[i] == True:
                self.inputData[self.inputData.columns[0]].iloc[i] = to_csv_data[i]
        return self.inputData
    
    def predict_result(self, model, data_iter, device, data):
        column_name = data.columns[0]
        imputation = self.evaluate(model, data_iter, device)
        scaler = StandardScaler()
        scaler = scaler.fit(data[column_name].to_numpy().reshape(-1,1))
        result = scaler.inverse_transform(imputation[0])
        return result[:, 0]

    def evaluate(self, model, data_iter, device):
        model.eval()
        imputations = []
        for idx, data in enumerate(data_iter):
            data = Brits_model.to_var(data, device)
            ret = model.run_on_batch(data, None)
            eval_masks = ret['eval_masks'].data.cpu().numpy()
            imputation = ret['imputations'].data.cpu().numpy()
            imputations += imputation[np.where(eval_masks == 1)].tolist()
        imputations = np.asarray(imputations)
        return imputation