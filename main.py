
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import setting

if __name__ == '__main__':
    ### input data preparation
    inputType ='influx' # or file
    input_data = setting.inputControl(inputType)
    
    ### preprocessing
    from KETIPrePartialDataPreprocessing import data_preprocessing
    partialP = data_preprocessing.packagedPartialProcessing(setting.process_param)
    output = partialP.allPartialProcessing(input_data)