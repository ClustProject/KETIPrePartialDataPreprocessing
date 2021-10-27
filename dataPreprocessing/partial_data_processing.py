class partialDataProcessing():
    def __init__(self):
        self.columnNaNCount={}
        self.columnNaNRatio={}
        
    def setData(self, data):
        self.data = data
        self.resultData = data.copy()
        self.totalLength = len(data)
        self.columns = data.columns
    
    def dataCleaning(self, imputation_parameter):
        self.imputation_parameter = imputation_parameter
        #Outlier2NaN = OutlierDetection.CertainOutlierDetection()
        clean_param={'flag':True, 'data_type':'air'}
        #Outlier Detection and let outlier be NaN
        self.dataWithMoreNaN = self.OutlierDetection(self.data, clean_param)
        for column in self.columns:
            column_data = self.dataWithMoreNaN[[column]] 
            column_data = self.columnImputation(column_data, column)
            self.resultData[column] = column_data
        return self.resultData
    
    # 옆에서 가져왔음, 수정해야함 
    def OutlierDetection(self, data_raw, clean_param):
        if clean_param['flag'] ==True:
            from KETIPrePartialDataPreprocessing.PartialDataCleansing.definite_error_detection import min_max_limit_value
            self.limit_min_max = min_max_limit_value.MinMaxLimitValueSet().get_data_min_max_limitSet(clean_param['data_type'])
            from KETIPrePartialDataPreprocessing.dataPreprocessing import MSOutlierDetection
            preprocessed_data = MSOutlierDetection.CertainOutlierDetection().get_valid_data(data_raw, self.limit_min_max)
            #preprocessed_data = MSOutlierDetection.uncertain_outlier_detection(preprocessed_data, column) 
            # Column Error
        else:
            preprocessed_data = data_raw.copy()
        return preprocessed_data
    
    def columnImputation(self, column_data, column):
                    
        # 2. Missing Pattern Detection Module
        from KETIPrePartialDataPreprocessing.dataPreprocessing import MissingPatternDetection
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
        from KETIPrePartialDataPreprocessing.dataPreprocessing import Imputation
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
            dataset = Imputer.cubic_interpolate(dataset, min_limi, max_limit)
    
        elif method == 'spline':
            dataset = Imputer.spline_interpolate(dataset,  min_limi, max_limit)

        elif method == 'barycentric':
            dataset = Imputer.barycentric_interpolate(dataset, min_limi, max_limit)

        elif method == 'polynomial':
            dataset = Imputer.polynomial_interpolate(dataset, min_limi, max_limit)
        return dataset