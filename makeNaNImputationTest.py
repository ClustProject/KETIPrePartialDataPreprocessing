
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
    
    imputation_param ={
    "imputation_method":[
        {"min":0,"max":1,"method":"mean"},
        {"min":2,"max":4,"method":"linear"},
        {"min":5,"max":10,"method":"brits"}],
    "totalNanLimit":0.3}
    refine_param = {'removeDuplication':True, 'staticFrequency':True}
    outlier_param= {'certainOutlierToNaN':True, 'uncertainOutlierToNaN':True, 'data_type':'air'}

    inputType ='influx' # and file
    input_data = inputControl(inputType)
    from data_preprocessing import DataPreprocessing
    MDP = DataPreprocessing()
    
    print('original', input_data.isna().sum())
    output_data = MDP.get_refinedData(input_data, refine_param)
    print('after refine', output_data.isna().sum())
    output_data = MDP.get_outlierToNaNData(output_data, outlier_param)
    print('after outlierDetection', output_data.isna().sum())

    """
    output_data = MDP.get_imputedData(output_data, imputation_param)
    print('after imputation', output_data.isna().sum())
    """
    
    



