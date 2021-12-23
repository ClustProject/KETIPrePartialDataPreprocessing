import numpy as np
import pandas as pd
  
class SerialImputation():
    """ This class applies a number of imputation techniques in series.
    """
    def __init__ (self):
        """ Define Imputation Methods
        """
        self.ScikitLearnMethods =['KNN','MICE']
        self.simpleMethods =['most_frequent', 'mean', 'median', ' constant']
        self.fillNAMethods = ['bfill','ffill']
        self.simpleIntMethods= ['linear', 'time', 'nearest', 'zero', 'slinear','quadratic', 'cubic', 'barycentric']
        self.orderIntMethods = [ 'polynomial', 'spline']
        self.deepMethods = ['brits']
 
    def get_dataWithSerialImputationMethods(self, data, imputation_param):
        """ This function cleans the data by applying several missing data handling methods.

        :param data: input data
        :type data: DataFrame 
        :param imputation_param: parameter of imputation
        :type imputation_param: json
        
        :return: NewDataframe output
        :rtype: DataFrame
        
        example
            >>> imputation_param = {'serialImputation': {'flag': True, 'imputation_method': [{'min': 0, 'max': 3, 'method': 'KNN', 'parameter': {}}, {'min': 4, 'max': 6, 'method': 'mean', 'parameter': {}}], 'totalNonNanRatio': 80}}
            >>> output = SerialImputation().get_dataWithSerialImputationMethods(data, imputation_param)
        """
        result = data.copy()
        imputation_method = imputation_param['imputation_method']
        totalNonNanRatio = imputation_param['totalNonNanRatio']
        # if total column NaN number is less tan limit, Impute it according to the parameter  
        result = self.dropOverNaNThresh(result, totalNonNanRatio)
        print("after Drop NaN Data")

        result = self.dfImputation(result, imputation_param)
        
        for column in data.columns:
            if column in result.columns:
                data.loc[:, column] = result[column]
        return data

    def dropOverNaNThresh(self, data, totalNonNanRatio):
        """ This function removes any column that does not meet the qualifications (total Non-Nan Ratio).

        :param data: input data
        :type data: DataFrame 
        :param totalNonNanRatio: total NaN Ratio (%). If the ratio of non-NaN values is less than or equal to the Ratio value, column data is removed.
        :type totalNonNanRatio: float(%)
        
        :return: NewDataframe excluding columns that do not meet the qualifications
        :rtype: DataFrame
        
        example
            >>> totalNonNanRatio = 80 # %
            >>> output = SerialImputation().dropOverNaNThresh(data, imputation_param)
        """
        totalNonNanNum = int(totalNonNanRatio/100 * len(data)) 
        result= data.dropna(thresh = totalNonNanNum, axis=1)
        print("totalNonNanNum:", totalNonNanNum)
        return result

    def printNaNDataSummary(self, data):
        """ Print Summary of data NaN status 

        :param data: input data
        :type data: DataFrame 
        
        example
            >>> output = SerialImputation().printNaNDataSummary(data)
        """
        nan_data_summary = round(data.isna().sum()/len(data), 2)
        print("===== NaN data Ratio summary ======")
        print(nan_data_summary)


    def dfImputation(self, data, imputation_param):
        """ This function returns final imputed data after imputation and filtering by max NaN limit.

        :param data: input_data
        :type data: DataFrame
        :param imputation_param: imputation_param
        :type imputation_param: json
        
        :return: NewDataframe after imputation and nan limit masking
        :rtype: DataFrame
        
        example
            >>> output = SerialImputation().dfImputation(data, imputation_param)
        """

        imputation_method = imputation_param['imputation_method']
        totalNonNanRatio = imputation_param['totalNonNanRatio']
        self.printNaNDataSummary(data)

        DataWithMaskedNaN = data.copy()
        for method_set in imputation_method:
            max_limit =method_set['max']
            from KETIPrePartialDataPreprocessing.data_imputation import nanMasking
            NaNInfoOverThresh= nanMasking.getConsecutiveNaNInfoOverThresh(data, max_limit)
            # Missing Data Imputation
            
            data = self.imputeDataByMethod(method_set, data)
            DataWithMaskedNaN = nanMasking.setNaNSpecificDuration(data, NaNInfoOverThresh, max_limit)
        self.printNaNDataSummary(DataWithMaskedNaN)
        return DataWithMaskedNaN

    def imputeDataByMethod(self, method_set, data):
        """ This function imputes data depending on method_set. (min, max, method, method_parameter)

        :param method_set: method information
        :type method_set: json
        :param data: input data
        :type data: DataFrame
        
        :return: NewDataframe after imputation
        :rtype: DataFrame
        
        example
            >>> method_set = {'min': 0, 'max': 3, 'method': 'KNN', 'parameter': {}}
            >>> output = SerialImputation().imputeDataByMethod(method_set, data)
        """
        
        min_limit = method_set['min']
        max_limit = method_set['max']
        method = method_set['method']
        parameter = method_set['parameter']


        from KETIPrePartialDataPreprocessing.data_imputation import basicMethod 
        from KETIPrePartialDataPreprocessing.data_imputation.DL import deepLearningImputation 
        basicImpute = basicMethod.BasicImputation(data, method, max_limit)
        if method in self.ScikitLearnMethods:
            result = basicImpute.ScikitLearnMethod()       
        elif method in self.simpleMethods:
            result = basicImpute.simpleMethod()
        elif method in self.simpleIntMethods:
            result = basicImpute.simpleIntMethod()
        elif method in self.fillNAMethods:
            result = basicImpute.fillNAMethod()
        elif method in self.orderIntMethods:
            result = basicImpute.orderIntMethod()
        elif method in self.deepMethods:
            result = deepLearningImputation.DLImputation(data, method, parameter).getResult()
        else:
            result = data.copy()
            print("Couldn't find a proper imputation method.")

        return result        