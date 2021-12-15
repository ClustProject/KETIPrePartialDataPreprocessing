import sys
import os
sys.path.append("../")
sys.path.append("../..")

class DataPreprocessing():
    def __init__(self):
        pass
    
    def get_refinedData(self, data, refine_param):
        # 1. Data Refining
        result = data.copy()
        if refine_param['removeDuplication']['flag']== True:
            from KETIPrePartialDataPreprocessing.data_refine import redundancy
            result = redundancy.ExcludeRedundancy(result).get_result()

        if refine_param['staticFrequency']['flag'] == True:
            from KETIPrePartialDataPreprocessing.data_refine import frequency
            inferred_freq = refine_param['staticFrequency']['frequency']
            result = frequency.FrequencyRefine(result, inferred_freq).get_result()   

        self.refinedData = result
        return self.refinedData
    
    def get_outlierToNaNData(self, data, outlier_param):
        from KETIPrePartialDataPreprocessing.outlier_detection import outlierToNaN
        self.datawithMoreCertainNaN, self.datawithMoreUnCertainNaN = outlierToNaN.OutlierToNaN(outlier_param).getDataWithNaN(data)
        return self.datawithMoreCertainNaN, self.datawithMoreUnCertainNaN

    def get_imputedData(self, data, imputation_param):
        if imputation_param['serialImputation']['flag'] == True:
            from KETIPrePartialDataPreprocessing.data_imputation import Imputation
            self.imputedData = Imputation.SerialImputation().get_dataWithSerialImputationMethods(data, imputation_param['serialImputation'])
        else:
            self.imputedData = data.copy()
        return self.imputedData
    # Add New Function

class packagedPartialProcessing(DataPreprocessing):
    def __init__(self, process_param):
        self.refine_param = process_param['refine_param']
        self.outlier_param = process_param['outlier_param']
        self.imputation_param = process_param['imputation_param']
     
    def allPartialProcessing(self, input_data):
        ###########
        refined_data = self.get_refinedData(input_data, self.refine_param)
        ###########
        datawithMoreCertainNaN, datawithMoreUnCertainNaN = self.get_outlierToNaNData(refined_data, self.outlier_param)
        ###########
        imputed_data = self.get_imputedData(datawithMoreUnCertainNaN, self.imputation_param)
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
    import setting
    ###
    ### input data 
    inputType ='file' # or file    
    from KETIPrePartialDataPreprocessing import main
    input_data = main.inputControl(inputType)
    ### function test
    MDP = DataPreprocessing()
    #result = MDP.get_refinedData(input_data, setting.refine_param)
    result = MDP.get_imputedData(input_data, setting.imputation_param)

    ###