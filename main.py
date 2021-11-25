
import sys
import os
sys.path.append("../")
sys.path.append("../..")

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
        "removeDuplication":{
            "flag":True
        },
        "staticFrequency":{
            "flag":True
        }
    }

    outlier_param  = {
        "certainOutlierToNaN":{
            "flag":True
        },
        "uncertainOutlierToNaN":{
            "flag":True,
            "param":{
                "neighbor":[
                    0.5,
                    0.6
                ]
            }
        },
        "data_type":"air"
    }
    imputation_param = {
    "serialImputation":{
        "flag":True,
        "imputation_method":[
            {
                "min":0,
                "max":50,
                "method":"linear"
            }
        ],
        "totalNanLimit":70
    }
}
    ###
    ### input
    inputType ='file' # or file    
    input_data = inputControl(inputType)
    ###
    from KETIPrePartialDataPreprocessing import data_preprocessing
    output = data_preprocessing.ByAllMethod(input_data, refine_param, outlier_param, imputation_param)