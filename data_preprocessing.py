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

    def get_imputedData(self, data, impuation_param):
        from KETIPrePartialDataPreprocessing.data_imputation import Imputation
        self.imputedData = Imputation.MultipleImputation().getDataWithMultipleImputation(data, impuation_param)
        return self.imputedData

# Data Cleaning Class
# Init -> SetData -> data Cleaning
def ByAllMethod(input_data, refine_param, outlier_param, imputation_param):

    MDP = DataPreprocessing()
    ###########
    refined_data = MDP.get_refinedData(input_data, refine_param)
    ###########
    datawithMoreCertainNaN, datawithMoreUnCertainNaN = MDP.get_outlierToNaNData(refined_data, outlier_param)
    ###########
    imputed_data = MDP.get_imputedData(datawithMoreUnCertainNaN, imputation_param)
    ###########
    result ={'original':input_data, 'refined_data':refined_data, 'datawithMoreCertainNaN':datawithMoreCertainNaN,
    'datawithMoreUnCertainNaN':datawithMoreUnCertainNaN, 'imputed_data':imputed_data}
    return result

 ## Get Multiple output
def MultipleDatasetByAllMethod(multiple_dataset, process_param):
    output={}
    refine_param = process_param['refine_param']
    outlier_param = process_param['outlier_param']
    imputation_param = process_param['imputation_param']
    for key in list(multiple_dataset.keys()):
        output[key] = ByAllMethod(multiple_dataset[key], refine_param, outlier_param, imputation_param)
    return output

