
import sys
import os
sys.path.append("../")
sys.path.append("../..")


def inputControl(inputType):
    from KETIPrePartialDataPreprocessing.data_manager.multipleDataSourceIngestion import getData
    dataC = getData()
    if inputType=="file":
        BASE_DIR = os.getcwd()
        input_file = os.path.join(BASE_DIR, 'data_miss_original.csv')
        input_data = dataC.getFileInput(input_file, 'timedate')
    elif inputType =="influx":
        input_data = dataC.getInfluxInput()

    return input_data

if __name__ == '__main__':
    ### Parameter Test
    inputType ='influx' # or file
    refine_param = {'removeDuplication':True, 'staticFrequency':True}
    outlier_param= {'certainOutlierToNaN':True, 'uncertainOutlierToNaN':True, 'data_type':'air'}
    """
    imputation_param ={
    "imputation_method":[
        {"min":0,"max":1,"method":"mean"},
        {"min":2,"max":4,"method":"linear"},
        {"min":5,"max":10,"method":"brits"}],
    "totalNanLimit":0.3}
    """
    imputation_param ={
    "imputation_method":[
        {"min":0,"max":1,"method":"mean"}],
    "totalNanLimit":30}
    
    input_data = inputControl(inputType)
    from KETIPrePartialDataPreprocessing import data_preprocessing
    output = data_preprocessing.get_preprocessed_data(input_data, refine_param, outlier_param, imputation_param)

    
    
    
    



