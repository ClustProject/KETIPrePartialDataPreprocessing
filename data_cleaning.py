import sys
import os
sys.path.append("../")
sys.path.append("../..")

# Data Cleaning Class
# Init -> SetData -> data Cleaning

class DataCleaning():
    def __init__(self):
        self.columnNaNCount={}
        self.columnNaNRatio={}
        
    def setData(self, data):
        self.data = data
        self.resultData = data.copy()
        self.totalLength = len(data)
        self.columns = data.columns

    def dataCleaning(self, imputation_parameter, outlier_param):
        self.imputation_parameter = imputation_parameter

        #Outlier Detection and let outlier be NaN
        from KETIPrePartialDataPreprocessing.outlier_detection import outlierToNaN
        self.dataWithMoreNaN = outlierToNaN.OutlierToNaN(self.data, outlier_param).getDataWithNaN()
        for column in self.columns:
            column_data = self.dataWithMoreNaN[[column]] 
            column_data = self._columnImputation(column_data, column)
            self.resultData[column] = column_data
        return self.resultData
    
    
    def _columnImputation(self, column_data, column):
                    
        # 2. Missing Pattern Detection Module
        from KETIPrePartialDataPreprocessing.data_imputation import MissingPatternDetection
        NaNPatternCheck = MissingPatternDetection.MissingPatternDetection()
        column_data = NaNPatternCheck.get_missing_pattern(column_data, column)

        # 3. Missing Data Imputation
        imputation_method = self.imputation_parameter['imputation_method']
        totalNanLimit = self.imputation_parameter['totalNanLimit']

        self.columnNaNCount[column]=self.data[column].isna().sum()
        self.columnNaNRatio[column]=round(float(self.columnNaNCount[column]*100/self.totalLength), 2)
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