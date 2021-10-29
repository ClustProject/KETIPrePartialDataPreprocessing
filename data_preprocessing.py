import sys
import os
sys.path.append("../")
sys.path.append("../..")

# Data Cleaning Class
# Init -> SetData -> data Cleaning
def get_preprocessed_data(input_data, refine_param, outlier_param, imputation_param):

    MDP = DataPreprocessing()
    ###########
    print('original', input_data.isna().sum())
    output_data = MDP.get_refinedData(input_data, refine_param)
    print('after refine', output_data.isna().sum())
    ###########
    output_data = MDP.get_outlierToNaNData(output_data, outlier_param)
    print('after outlierDetection', output_data.isna().sum())
    ###########
    """
    ### TODO ST Oh
    output_data = MDP.get_imputedData(output_data, imputation_param)
    print('after imputation', output_data.isna().sum())
    """
    return output_data
    
class DataPreprocessing():
    """
    This class provides method to clean Data
    1) duplicated_data_remove: Remove duplicated part
    2) make_static_fequency: Generate data with static frequency inferred from the original data
    3) 
    """
    def __init__(self):
        pass

    def get_refinedData(self, data, refine_param):
        self.refineData = data.copy()
        from KETIPrePartialDataPreprocessing.data_cleaning import data_refine
        # 1. Data Refining
        if refine_param['removeDuplication'] == True:
            self.refineData = data_refine.duplicate_data_remove(self.refineData)
        if refine_param['staticFrequency'] == True:
            # TODO extending static frequency function 
            self.refineData = data_refine.make_static_frequency(self.refineData)
        return self.refineData
    
    def get_outlierToNaNData(self, data, outlier_param):
        from KETIPrePartialDataPreprocessing.outlier_detection import outlierToNaN
        self.get_outlierToNaNResult = outlierToNaN.OutlierToNaN(data, outlier_param).getDataWithNaN()
        return self.get_outlierToNaNResult

    def get_imputedData(self, data, impuation_param):
        result = data.copy()
        for column in data.columns:
            column_data = data[[column]] 
            column_data = self.columnImputation(column_data, column, impuation_param)
            print(column_data)
            result[column] = column_data
        return result

    ## 아래 두 function은 코딩 Release 후에 imputation package 쪽으로 가는게 맞아 보임 나중에 이야기
    def columnImputation(self, column_data, column, imputation_parameter):
        self.columnNaNCount={}
        self.columnNaNRatio={}          
        totalLength = len(column_data)
        # 2. Missing Pattern Detection Module
        from KETIPrePartialDataPreprocessing.data_imputation import MissingPatternDetection
        NaNPatternCheck = MissingPatternDetection.MissingPatternDetection()
        column_data = NaNPatternCheck.get_missing_pattern(column_data, column)

        # 3. Missing Data Imputation
        imputation_method = imputation_parameter['imputation_method']
        totalNanLimit = imputation_parameter['totalNanLimit']

        self.columnNaNCount[column]=column_data.isna().sum()
        print(self.columnNaNCount[column])
        self.columnNaNRatio[column]=round(float(self.columnNaNCount[column]*100/totalLength), 2)
        if (self.columnNaNRatio[column] < totalNanLimit):
        # if total column NaN number is less tan limit, Impute it according to the parameter    
            for method_set in imputation_method:
                # 3. Missing Data Imputation
                column_data = self.imputeDataByMethod(method_set, column_data)
        return column_data

    
    #def outlierToNaN(self, data)
    def imputeDataByMethod(self, method_set, dataset):
        min_limit = method_set['min']
        max_limit = method_set['max']
        method = method_set['method']
        from KETIPrePartialDataPreprocessing.data_imputation import Imputation

        Imputer = Imputation.imputation_methods()
        if method == 'mean':
            dataset = Imputer.mean_interpolate(dataset, min_limit, max_limit)

        elif method == 'median':
            dataset = Imputer.median_interpolate(dataset, min_limit, max_limit)

        elif method == 'bfill':
            dataset = Imputer.bfill(dataset, min_limit, max_limit)

        elif method == 'ffill':    
            dataset = Imputer.ffill(dataset,  min_limit, max_limit)

        if method == 'linear':
            dataset = Imputer.linear_interpolate(dataset,  min_limit, max_limit)
        
        elif method == 'time':
            dataset = Imputer.time_interpolation(dataset,  min_limit, max_limit)

        elif method == 'nearest':
            dataset = Imputer.nearest_interpolate(dataset, min_limit, max_limit)

        elif method == 'zero':
            dataset = Imputer.zero_interpolate(dataset, min_limit, max_limit)

        elif method == 'slinear':
            dataset = Imputer.slinear_interpolate(dataset, min_limit, max_limit)

        elif method == 'quadratic':
            dataset = Imputer.quadratic_interpolate(dataset, min_limit, max_limit)

        elif method == 'cubic':
            dataset = Imputer.cubic_interpolate(dataset, min_limit, max_limit)
    
        elif method == 'spline':
            dataset = Imputer.spline_interpolate(dataset,  min_limit, max_limit)

        elif method == 'barycentric':
            dataset = Imputer.barycentric_interpolate(dataset, min_limit, max_limit)

        elif method == 'polynomial':
            dataset = Imputer.polynomial_interpolate(dataset, min_limit, max_limit)
        return dataset