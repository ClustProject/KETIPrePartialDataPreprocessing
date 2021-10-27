import numpy as np
import pandas as pd
import sys
import os
sys.path.append("../")
sys.path.append("../..")

if __name__ == '__main__':
    BASE_DIR = os.getcwd()
    input_file = os.path.join(BASE_DIR, 'KETIPrePartialDataPreprocessing', 'dataPreProcessing','data_miss_original.csv')
    imputation_parameter ={
    "imputation_method":[
        {
            "min":0,
            "max":1,
            "method":"mean"
        },
        {
            "min":2,
            "max":4,
            "method":"linear"
        },
        {
            "min":5,
            "max":10,
            "method":"brits"
        }
    ],
        "totalNanLimit":0.3
    }

    from dataIngestion import getData
    input_data = getData().getFileInput(input_file, 'timedate')
    test_data = input_data[:10000]
    from partial_data_processing import partialDataProcessing
    MDP = partialDataProcessing()
    MDP.setData(test_data)
    output_data = MDP.dataCleaning(imputation_parameter)



