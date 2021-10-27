
import sys
import os
sys.path.append("../")
sys.path.append("../..")

def inputControl(inputType):
    dataC = getData()
    if inputType=="file":
        BASE_DIR = os.getcwd()
        input_file = os.path.join(BASE_DIR, 'data_miss_original.csv')
        input_data = dataC.getFileInput(input_file, 'timedate')
    elif inputType =="influx":
        input_data = dataC.getInfluxInput()

    return input_data

if __name__ == '__main__':
    
    imputation_param ={
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

    outlier_remove_param={'flag':True, 'data_type':'air', 'uncertain_outlier_remove':False, 'staticFrequency':True}
    from KETIPrePartialDataPreprocessing.data_manager.multipleDataSourceIngestion import getData

    inputType ='influx' # and file
    input_data = inputControl(inputType)
    from data_cleaning import DataCleaning
    MDP = DataCleaning()
    MDP.setData(input_data)
    
    output_data = MDP.dataCleaning(imputation_param, outlier_remove_param)
    print(input_data.isna().sum())
    print(output_data.isna().sum())



