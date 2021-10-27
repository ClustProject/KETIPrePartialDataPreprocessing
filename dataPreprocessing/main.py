import numpy as np
import pandas as pd
import sys
sys.path.append("../")
sys.path.append("../..")


if __name__ == '__main__':
    input_file = './data_miss_original.csv'
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

    from KETIPrePartialDataPreprocessing.dataPreprocessing.dataIngestion import getData
    from KETIPrePartialDataPreprocessing.dataPreprocessing.partial_data_processing import partialDataProcessing

    input_data = getData().getFileInput(input_file, 'timedate')
    MDP = partialDataProcessing()
    MDP.setData(input_data[:10000])
    output_data = MDP.dataCleaning(imputation_parameter)



