
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import setting
    
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
    
    ### input
    inputType ='file' # or file    
    input_data = inputControl(inputType)
    ### test
    from KETIPrePartialDataPreprocessing import data_preprocessing
    partialP = data_preprocessing.packagedPartialProcessing(setting.process_param)
    output = partialP.allPartialProcessing(input_data)

