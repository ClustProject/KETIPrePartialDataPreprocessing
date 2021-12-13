import sys
import os
sys.path.append("../")
sys.path.append("../..")

class DataPreprocessing():
    def __init__(self):
        pass
    
    def get_refinedData(self, data, refine_param):
        from KETIPrePartialDataPreprocessing.data_cleaning import data_refine
        # 1. Data Refining
        self.refinedData = data_refine.RefineData().makeRefineData(data, refine_param)
        return self.refinedData
    
    def get_outlierToNaNData(self, data, outlier_param):
        from KETIPrePartialDataPreprocessing.outlier_detection import outlierToNaN
        self.datawithMoreCertainNaN, self.datawithMoreUnCertainNaN = outlierToNaN.OutlierToNaN(outlier_param).getDataWithNaN(data)
        return self.datawithMoreCertainNaN, self.datawithMoreUnCertainNaN

    def get_imputedData(self, data, imputation_param):
        if imputation_param['serialImputation']['flag'] == True:
            print("SerialImputation")
            from KETIPrePartialDataPreprocessing.data_imputation import Imputation
            self.imputedData = Imputation.SerialImputation().getDataWithSerialImputation(data, imputation_param['serialImputation'])
        else:
            self.imputedData = data.copy()
        return self.imputedData

    # Add New Function


class packagedPartialProcessing():
    def __init__(self, process_param):
        self.refine_param = process_param['refine_param']
        self.outlier_param = process_param['outlier_param']
        self.imputation_param = process_param['imputation_param']
     
    def allPartialProcessing(self, input_data):
        MDP = DataPreprocessing()
        ###########
        refined_data = MDP.get_refinedData(input_data, self.refine_param)
        ###########
        datawithMoreCertainNaN, datawithMoreUnCertainNaN = MDP.get_outlierToNaNData(refined_data, self.outlier_param)
        ###########
        imputed_data = MDP.get_imputedData(datawithMoreUnCertainNaN, self.imputation_param)
        ###########
        result ={'original':input_data, 'refined_data':refined_data, 'datawithMoreCertainNaN':datawithMoreCertainNaN,
        'datawithMoreUnCertainNaN':datawithMoreUnCertainNaN, 'imputed_data':imputed_data}
        return result

    ## Get Multiple output
    def MultipleDatasetallPartialProcessing(self, multiple_dataset):
        output={}
        for key in list(multiple_dataset.keys()):
            output[key] = self.allPartialProcessing(multiple_dataset[key])
        return output

if __name__ == '__main__':
    ### Parameter Test
    refine_param = {
    "removeDuplication":{"flag":True},
    "staticFrequency":{"flag":True}
    }
    outlier_param  = {
        "certainOutlierToNaN":{"flag":True},
        "uncertainOutlierToNaN":{
            "flag":True,
            "param":{"neighbor":[0.3,0.3]}
        },
        "data_type":"air"
    }
    imputation_param = {
        "serialImputation":{
            "flag":True,
            "imputation_method":[{"min":0,"max":2,"method":"mean" , "parameter":{}}],
            "totalNanLimit":90
        }
    }
    ###
    ### input data 
    inputType ='file' # or file    
    from KETIPrePartialDataPreprocessing import main
    input_data = main.inputControl(inputType)
    ### function test
    from KETIPrePartialDataPreprocessing import data_preprocessing
    MDP = DataPreprocessing()
    ###########
    refined_data = MDP.get_refinedData(input_data, refine_param)
    print(refined_data)
    ###