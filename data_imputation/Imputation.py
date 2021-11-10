import numpy as np
import pandas as pd


class MultipleImputation():
    def __init__ (self):
        self.ScikitLearnMethods =['KNN','MICE']
        self.simpleMethods =['most_frequent', 'mean', 'median', ' constant']
        self.fillNAMethods = ['bfill','ffill']
        self.simpleIntMethods= ['linear', 'time', 'nearest', 'zero', 'slinear','quadratic', 'cubic', 'barycentric']
        self.orderIntMethods = [  'polynomial', 'spline']


    def getDataWithMultipleImputation(self, data, imputation_param):
        result = data.copy()
        self.imputation_param = imputation_param
        for column in data.columns:
            column_data = data[[column]]
            column_data = self.columnImputation(column_data, column, imputation_param)
            result[column] = column_data
        return result

    def columnImputation(self, column_data, column, imputation_parameter):
            self.columnNaNCount={}
            self.columnNaNRatio={}          
            totalLength = len(column_data)
            
            imputation_method = imputation_parameter['imputation_method']
            totalNanLimit = imputation_parameter['totalNanLimit']
            self.columnNaNCount[column]=column_data.isna().sum()
            self.columnNaNRatio[column]= round(float(self.columnNaNCount[column]/totalLength)*100,2)
            print("NaN Ratio:", column, self.columnNaNRatio[column],"%")
            if (self.columnNaNRatio[column] < totalNanLimit):
            # if total column NaN number is less tan limit, Impute it according to the parameter    
                for method_set in imputation_method:
                    # 3. Missing Data Imputation
                    column_data = self.imputeDataByMethod(method_set, column_data)
            return column_data

        
    #def outlierToNaN(self, data)
    def makeDF(self, data, series_result):
        dfResult = pd.DataFrame(series_result, columns = data.columns, index = data.index)
        return dfResult

    def imputeDataByMethod(self, method_set, data):
        
        min_limit = method_set['min']
        max_limit = method_set['max']
        method = method_set['method']
        print(method)
        # Get Input Nan Locatoin Info
        from KETIPrePartialDataPreprocessing.data_imputation import nanMasking
        column_name= data.columns[0]
        NaNInfoOverThresh = list(nanMasking.getConsecutiveNaNInfoOverThresh(data, column_name, max_limit))
        column_data = data[column_name].values
        column_data = column_data.reshape(-1, 1)

        from KETIPrePartialDataPreprocessing.data_imputation import basicMethod 
        if method in self.ScikitLearnMethods:
            result = basicMethod.ScikitLearnMethod(column_data, method, max_limit)
            result = self.makeDF(data, result)
        elif method in self.simpleMethods:
            result = basicMethod.simpleMethod(column_data, method, max_limit)
            result = self.makeDF(data, result)
        elif method in self.simpleIntMethods:
            result = basicMethod.simpleIntMethod(data, method, max_limit)
        elif method in self.fillNAMethods:
            result = basicMethod.fillNAMethod(data, method, max_limit)
        elif method in self.orderIntMethods:
            result = basicMethod.orderIntMethod(data, method, max_limit)
        else:
            result = data.copy()
            print("Couldn't find a proper imputation method.")

        # Data Masking
        DataWithMaskedNaN = nanMasking.setNaNSpecificDuration(result, column_name, NaNInfoOverThresh, max_limit)
        return DataWithMaskedNaN

# from sklearn.impute import SimpleImputer, KNNImputer, IterativeImputer
# from sklearn.experimental import enable_iterative_imputer

# temp_miss = temp_miss.assign(temp_na_mean = lambda x: SimpleImputer(strategy='mean').fit_transform(x[['temp']]),
#                                temp_na_median = lambda x: SimpleImputer(strategy='median').fit_transform(x[['temp']]),
#                                temp_na_most_frequent = lambda x: SimpleImputer(strategy='most_frequent').fit_transform(x[['temp']]),
#                                temp_na_last = lambda x: x['temp'].fillna(method='f   fill'),
#                                temp_na_next = lambda x: x['temp'].fillna(method='bfill'),
#                                temp_na_last_next = lambda x: x[['temp_na_last', 'temp_na_next']].mean(axis=1),
#                                temp_na_knn = lambda x: KNNImputer(n_neighbors=3, weights='distance').fit_transform(x[['temp']])[:, 0],
#                                temp_na_iterative = lambda x: IterativeImputer().fit_transform(x[['temp']])[:, 0],
#                                temp_na_zero = lambda x: SimpleImputer(fill_value=0.0, strategy='constant').fit_transform(x[['temp']])
#                                )