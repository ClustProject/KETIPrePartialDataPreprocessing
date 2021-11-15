import sys
import os
import numpy as np
import torch
from inference import inference, model_load
from training import training
import Brits_model

sys.path.append("../")
sys.path.append("../..")

if __name__ == "__main__":
    db_name = 'air_indoor_경로당'
    ms_name = 'ICL1L2000234'

    inputType = 'influx'
    input_limit = 10000
    column_name = 'in_temp'
    deepLearningModel = 'brits'
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    # 좋은 데이터로 시작
    from KETIPrePartialDataPreprocessing import main
    training_data = main.inputControl(inputType)[:input_limit]
    training_data = training_data[[column_name]]
    frequent_value = training_data.value_counts().idxmax()
    training_data = training_data.replace(frequent_value, np.nan)
    data_iter = Brits_model.get_loader('./data_imputation/brits/brits_json/data.json', batch_size=64)
    # root = os.listdir()
    root = os.getcwd()
    saved_model_name = os.path.join(root, db_name, ms_name, deepLearningModel, column_name + '.pt')
    print(saved_model_name)

    model = training(training_data, saved_model_name)

    result = inference.inference(model, data_iter, device, training_data)
    to_csv_data = result.tolist()
    nan_data = training_data[column_name].isnull()
    for i in range(len(nan_data)):
        if nan_data.iloc[i] == True:
            training_data[column_name].iloc[i] = to_csv_data[i]
    training_data.to_csv("./imputated_data.csv", index=False)
    # ####
    # 좋은 데이터에 임의로 이상한 값 넣기
    # test_data = main.inputControl(inputType)[input_limit:output_limit]
    # test_frequent_value = test_data.value_counts().idxmax()
    # test_data = test_data.replace(test_frequent_value, np.nan)

    # test_data 그리기
