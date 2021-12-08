import sys
import os
import numpy as np
import torch
from inference import inference, model_load
from training import training
import Brits_model
import copy 

sys.path.append("../")
sys.path.append("../..")

if __name__ == "__main__":
    db_name = 'air_indoor_경로당'
    ms_name = 'ICL1L2000234'
    inputType = 'influx'
    input_limit = 1000
    column_name = 'in_temp'
    deepLearningModel = 'brits'
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    """
    
    """
    from KETIPrePartialDataPreprocessing import main
    training_data = main.inputControl(inputType)[:input_limit]
    training_data = training_data[[column_name]]
    frequent_value = training_data.value_counts().idxmax()
    training_data = training_data.replace(frequent_value, np.nan)
    training_data = training_data.replace(-9999.0, np.nan)
    
    training_data.to_csv("./original_data.csv", index=True)
    
    test_data = training_data[300:500]
    test_data.to_csv("./test_original_data2.csv", index=True)

    json_path = './data_imputation/brits/brits_json/' + os.path.join(db_name, ms_name)
    json_data_path = json_path + '/' + column_name + '.json'
    os.makedirs(json_path , exist_ok=True)

    
    # json data 생성
    Brits_model.makedata(training_data, json_data_path)

    data_iter = Brits_model.get_loader(json_data_path, batch_size=64)
    # root = os.listdir()
    root = os.getcwd()
    saved_model_path = os.path.join(root, db_name, ms_name, deepLearningModel)
    saved_model_name = column_name+'.pth'
    os.makedirs(saved_model_path , exist_ok=True)
    print(saved_model_path)

    model = training(training_data, data_iter, json_data_path, saved_model_path, saved_model_name)
    
    loaded_model = Brits_model.Brits_i(108, 1, 0, len(test_data), device).to(device)
    loaded_model.load_state_dict(copy.deepcopy(torch.load(saved_model_path + '/' + saved_model_name, device)))

    result = inference(loaded_model, data_iter, device, test_data)
    to_csv_data = result.tolist()
    nan_data = test_data[column_name].isnull()
    for i in range(len(nan_data)):
        if nan_data.iloc[i] == True:
            test_data[column_name].iloc[i] = to_csv_data[i]
    
    test_data.to_csv("./test_imputed_data2.csv", index=True)