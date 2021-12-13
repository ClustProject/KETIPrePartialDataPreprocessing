
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

def inputControl(inputType):
    from KETIPrePartialDataPreprocessing.data_manager.multipleDataSourceIngestion import getData
    dataC = getData()
    if inputType=="file":
        BASE_DIR = os.getcwd()
        input_file = os.path.join(BASE_DIR, 'sampleData', 'data_miss_original.csv')
        input_data = dataC.getFileInput(input_file, 'timedate')
    elif inputType =="influx":
        db_name  = 'air_indoor_경로당'
        ms_name = 'ICL1L2000235' 
        input_data = dataC.getInfluxInput(db_name, ms_name)

    return input_data

if __name__ == '__main__':
    ### Parameter Test
    inputType ='influx' # or file
    refine_param = {
        "removeDuplication":{"flag":True},
        "staticFrequency":{"flag":True}
    }
    outlier_param  = {
        "certainOutlierToNaN":{"flag":True},
        "uncertainOutlierToNaN":{"flag":True,"param":{"neighbor":[0.5, 0.6]}},
        "data_type":"air"
    }
    column_name ='in_temp'
    model_folder = os.path.join(os.getcwd(),'data_imputation','DL','brits', 'model', 'air_indoor_경로당', 'ICL1L2000234')
    imputation_param = {
    "serialImputation":{
        "flag":True,
        "imputation_method":[{"min":0,"max":2,"method":"linear", "parameter":{}}, 
                             {"min":3,"max":6,"method":"brits", "parameter":{"model_address":model_folder}}],"totalNanLimit":90}
    }
    process_param = {'refine_param':refine_param, 'outlier_param':outlier_param, 'imputation_param':imputation_param}
    ###
    ### input
    inputType ='file' # or file    
    input_data = inputControl(inputType)
    ###
    from KETIPrePartialDataPreprocessing import data_preprocessing
    
    partialP = data_preprocessing.packagedPartialProcessing(process_param)
    output = partialP.allPartialProcessing(input_data)

