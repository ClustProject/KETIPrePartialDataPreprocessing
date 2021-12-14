import numpy as np
import pandas as pd
  
class SerialImputation():
    def __init__ (self):
        self.ScikitLearnMethods =['KNN','MICE']
        self.simpleMethods =['most_frequent', 'mean', 'median', ' constant']
        self.fillNAMethods = ['bfill','ffill']
        self.simpleIntMethods= ['linear', 'time', 'nearest', 'zero', 'slinear','quadratic', 'cubic', 'barycentric']
        self.orderIntMethods = [ 'polynomial', 'spline']
        self.deepMethods = ['brits']
    """
    def getDataWithSerialImputation(self, data, imputation_param):
        result = data.copy()
        self.imputation_param = imputation_param
        for column in data.columns:
            column_data = data[[column]]
            column_data = self.columnImputation(column_data, column, imputation_param)
            result[column] = column_data
        return result
    """
    def getDataWithSerialImputation(self, data, imputation_param):
        result = data.copy()
        imputation_method = imputation_param['imputation_method']
        totalNanLimit = imputation_param['totalNanLimit']
        # if total column NaN number is less tan limit, Impute it according to the parameter  
        result= result.dropna(thresh=totalNanLimit, axis=1)
        result = self.dfImputation(result, imputation_param)

        for column in data.columns:
            if column in result.columns:
                data.loc[:, column] = result[column]
        return result

    def dfImputation(self, data, imputation_param):

        imputation_method = imputation_param['imputation_method']
        totalNanLimit = imputation_param['totalNanLimit']
        nan_data_summary = round(data.isna().sum()/len(data), 2)
        print("===== NaN data Ratio summary ======")
        print(nan_data_summary)

        DataWithMaskedNaN = data.copy()
        for method_set in imputation_method:
            max_limit =method_set['max']
            from KETIPrePartialDataPreprocessing.data_imputation import nanMasking
            NaNInfoOverThresh= nanMasking.getConsecutiveNaNInfoOverThresh(data, max_limit)
            # Missing Data Imputation
            print(data.isna().sum())
            data = self.imputeDataByMethod(method_set, data)
            print(data.isna().sum())
            DataWithMaskedNaN = nanMasking.setNaNSpecificDuration(data, NaNInfoOverThresh, max_limit)

        return DataWithMaskedNaN

    def columnImputation(self, column_data, column, imputation_param):
            self.columnNaNCount={}
            self.columnNaNRatio={}          
            totalLength = len(column_data)
            
            imputation_method = imputation_param['imputation_method']
            totalNanLimit = imputation_param['totalNanLimit']
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
        print(method_set)
        
        min_limit = method_set['min']
        max_limit = method_set['max']
        method = method_set['method']
        parameter = method_set['parameter']
        """      
        # Get Input Nan Locatoin Info
        from KETIPrePartialDataPreprocessing.data_imputation import nanMasking
        column_name= data.columns[0]
        NaNInfoOverThresh = list(nanMasking.getConsecutiveNaNInfoOverThresh(data, max_limit))
        column_data = data[column_name].values
        column_data = column_data.reshape(-1, 1)
        """
        from KETIPrePartialDataPreprocessing.data_imputation import basicMethod 
        if method in self.ScikitLearnMethods:
            # use numpy ndarray input (column_data)
            result = basicMethod.ScikitLearnMethod(data, method, max_limit)
            result = self.makeDF(data, result)
        elif method in self.simpleMethods:
            result = basicMethod.simpleMethod(data, method, max_limit)
            result = self.makeDF(data, result)
        elif method in self.simpleIntMethods:
            # use dataframe (data)
            result = basicMethod.simpleIntMethod(data, method, max_limit)
        elif method in self.fillNAMethods:
            result = basicMethod.fillNAMethod(data, method, max_limit)
        elif method in self.orderIntMethods:
            result = basicMethod.orderIntMethod(data, method, max_limit)
        elif method in self.deepMethods:
            from KETIPrePartialDataPreprocessing.data_imputation.DL import deepLearningImputation 
            result = deepLearningImputation.DLImputation(data, method, parameter).getResult()
        else:
            result = data.copy()
            print("Couldn't find a proper imputation method.")
        """
        # Data Masking
        DataWithMaskedNaN = nanMasking.setNaNSpecificDuration(result, NaNInfoOverThresh, max_limit)
        """
        return result        