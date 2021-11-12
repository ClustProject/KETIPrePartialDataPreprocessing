import sys
import os
import numpy as np
from inference import inference, model_load
from training import training, model_save

sys.path.append("../")
sys.path.append("../..")

if __name__ == "__main__":
    db_name = 'air_indoor_경로당'
    ms_name = 'ICL1L2000234'

    inputType = 'influx'
    input_limit = 100000
    output_limit = 101000
    column_name = 'in_temp'
    deepLearningModel = 'brits'
    
    # 좋은 데이터로 시작
    from KETIPrePartialDataPreprocessing import main
    training_data = main.inputControl(inputType)[:input_limit]
    training_data = training_data[[column_name]]

    # 수정하면서

    # root = os.listdir()
    root = os.getcwd()
    saved_model_name = os.path.join(root, db_name, ms_name, deepLearningModel, column_name + '.pt')
    print(saved_model_name)

    model = training(training_data, saved_model_name)
    # model_save(model)

    # ####
    # 좋은 데이터에 임의로 이상한 값 넣기
    test_data = main.inputControl(inputType)[input_limit:output_limit]
    test_frequent_value = test_data.value_counts().idxmax()
    test_data = test_data.replace(test_frequent_value, np.nan)
    # test_data 그리기
    model = model_load(saved_model_name)
    output = inference(test_data, model)
    # output_data 그리기

"""
1. (~11/10) Training 완성
2. (~11/11) Inference 완성
"""
