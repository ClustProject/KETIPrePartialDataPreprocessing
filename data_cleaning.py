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

    def _duplicate_data_remove(self, data):
        # duplicated Column, Index Drop
        data = data.sort_index()
        data = data.loc[:, ~data.columns.duplicated()]
        first_idx = data.first_valid_index()
        last_idx = data.last_valid_index()
        valid_data = data.loc[first_idx:last_idx]
        valid_data = valid_data.drop_duplicates(keep='first')
           
        return valid_data

    def make_static_frequency(self, data):
        # This function make static frequency 
        data_staticFrequency = data.copy()
        if len(data)> 2:
            #inferred_freq = pd.infer_freq(data_partial_raw[:5])
            inferred_freq = (data.index[1]-data.index[0])
            data_staticFrequency = data.asfreq(freq=inferred_freq)
        return data_staticFrequency

    def dataCleaning(self, imputation_parameter, outlier_param):
        self.imputation_parameter = imputation_parameter

        #Outlier Detection and let outlier be NaN
        from KETIPrePartialDataPreprocessing.outlier_detection import outlierToNaN
        self.dataWithMoreNaN = self.data.copy()
        self.dataWithMoreNaN = self._duplicate_data_remove(self.dataWithMoreNaN)
        if outlier_param['staticFrequency'] == True:
            self.dataWithMoreNaN = self.make_static_frequency(self.dataWithMoreNaN)
        self.dataWithMoreNaN = outlierToNaN.OutlierToNaN(self.dataWithMoreNaN, outlier_param).getDataWithNaN()
        """
        for column in self.columns:
            column_data = self.dataWithMoreNaN[[column]] 
            column_data = self._columnImputation(column_data, column)
            self.resultData[column] = column_data
        """
        self.resultData = self.dataWithMoreNaN 
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