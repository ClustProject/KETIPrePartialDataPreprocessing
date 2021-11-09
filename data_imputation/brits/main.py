import sys
import os
sys.path.append("../")
sys.path.append("../..")

def training(data, model_address):
    # TODO
    # model training
    # model_address 에 model 저장
    model = None
    return model

def model_save(model_name, model):
    # folder가 있을 경우 하위에 생성, 이미 있는 파일은 삭제
    # folder가 없을 경우 임의로 폴더 생성 
    pass

########

def model_load(model_name):
    # TODO 
    # model을 로드하여 전달함
    model = model_name
    return model

def inference(data, model):
    # TODO
    # model을 불러온 후 data를 imputation하고 결과를 전달

    result = data
    return result

import numpy as np
if __name__ == "__main__":
    db_name = 'air_indoor_경로당'
    ms_name = 'ICL1L2000234'

    inputType = 'file'
    input_limit = 100000
    column_name = 'temp'
    deepLearningModel = 'brits'
    
    # 좋은 데이터로 시작
    from KETIPrePartialDataPreprocessing import main
    training_data = main.inputControl(inputType)[:input_limit]
    training_data = training_data[[column_name]]

    # 수정하면서
    root =os.dir()
    saved_model_name = os.join(root, db_name, ms_name, deepLearningModel, column_name+'.h5') 
    model = training(training_data, saved_model_name)
    model_save (model)

    ####
    # 좋은 데이터에 임의로 이상한 값 넣기
    test_data = main.inputControl(inputType)[input_limit:]
    test_data = test_data.replace(4.0, np.nan)
    # test_data 그리기
    model = model_load(saved_model_name)
    output = inference(test_data, model)
    # output_data 그리기

"""
1. (~11/10) Training 완성
2. (~11/11) Inference 완성
"""
