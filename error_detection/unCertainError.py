from KETIPrePartialDataPreprocessing.error_detection import dataOutlier
import numpy as np
class unCertainErrorRemove():
    '''Let UnCertain Outlier from DataFrame Data to NaN. This function makes more Nan according to the data status.
    
    **Data Preprocessing Modules**::

            neighbor_error_detected_data
    '''
    def __init__(self, data, param):
  
        self.param = param
        data_outlier = dataOutlier.DataOutlier(data)
        self.data = data_outlier.refinmentForOutlierDetection()
    
    def getNoiseIndex(self):
        """    
        :return result: Noise Index
        :type: json

        self.outlierIndex
        self.mergedOutlierIndex

        """
        outlierDetectorConfigs =self.param['outlierDetectorConfig']
        MLList = [ 'IF', 'KDE', 'LOF', 'MoG', 'SR']
        self.outlierIndex={}
        for outlierDetectorConfig in outlierDetectorConfigs:
            print(outlierDetectorConfig)
            algorithm = outlierDetectorConfig['algorithm']
            print(algorithm)
            if algorithm in MLList:
                IndexResult = self.getOutlierIndexByMLOutlierDetector(outlierDetectorConfig)
            elif algorithm == "IQR" :
                IndexResult  = self.getOutlierIndexByIQR(outlierDetectorConfig)
            elif algorithm == "SD":
                IndexResult  = self.getOutlierIndexBySeasonalDecomposition(outlierDetectorConfig['alg_parameter'])
            self.outlierIndex[algorithm] = IndexResult 
        
        self.mergedOutlierIndex={}
        for column in self.data.columns:
            self.mergedOutlierIndex[column]= []
            for outlierDetectorConfig in outlierDetectorConfigs:
                algorithm = outlierDetectorConfig['algorithm']
                self.mergedOutlierIndex[column].extend(self.outlierIndex[algorithm][column])
        
        return self.mergedOutlierIndex

    def getIntersectionIndex(self, outlierIndex):
        """    
        :param outlierIndex: Noise Index
        :type outlierIndex: json

        :return intersectionIndex: Intersection index by each noise index key
        :type: list
        """
        first_key= list(outlierIndex.keys())[0]
        intersectionIndex = outlierIndex[first_key]
        for key, value in outlierIndex.items():
            intersectionIndex = list(set(intersectionIndex) & set(list(value)))
        return intersectionIndex

    def getOutlierIndexByIQR(self, param):
        """    
        :param param: having 'weight' parameter. weight is IQR duration adjustment parameter.
        :type weight: json

        :return outlier_index: Intersection index by each noise index key
        :type: list
        """
        df = self.data.copy()
        weight = param['alg_parameter']['weight']
        print(weight)
        outlier_index={}
        for column in df.columns:
            column_x = df[column]
            # 1/4 ????????? 3/4 ?????? ????????? np.percentile??? ??????
            quantile_25 = np.nanpercentile(column_x.values, 25)
            quantile_75 = np.nanpercentile(column_x.values, 75)
            print(quantile_25, quantile_75)

            # IQR??? ????????? IQR??? 1.5??? ?????? ???????????? ????????? ?????? ??????.
            iqr = quantile_75 - quantile_25
            iqr_weight = iqr * weight
            lowest_val = quantile_25 - iqr_weight
            highest_val = quantile_75 + iqr_weight

            # ??????????????? ?????????, ??????????????? ?????? ?????? ????????? ???????????? ???????????? Dataframe index ??????
            outlier_index[column] = column_x[(column_x < lowest_val) | (column_x > highest_val)].index
            print(lowest_val, highest_val)
        return outlier_index

    def getOutlierIndexBySeasonalDecomposition(self, outlierDetectorConfig):
        """    
        :param outlierDetectorConfig: have period and limit information ex> {"period":60*24, "limit":10}
        :type outlierDetectorConfig: json

        :return outlier_index: Intersection index by each noise index key
        :type: list
        """

        period = outlierDetectorConfig['period']
        limit = outlierDetectorConfig['limit']

        from statsmodels.tsa.seasonal import seasonal_decompose
        data_outlier = dataOutlier.DataOutlier(self.data)
        data_imputed = data_outlier.imputationForOutlierDetection()

        outlier_index={}
        for feature in data_imputed.columns:
            result = seasonal_decompose(data_imputed[feature],model='additive', period = period)
            n = result.seasonal.mean()+result.trend.mean()
            n = abs(n *limit)
            print("Limit Num:", n)
            NoiseIndex = result.resid[abs(result.resid)> n].index
            outlier_index[feature]= NoiseIndex
            import matplotlib.pyplot as plt
            result.plot()
            plt.show()
            
        return outlier_index

    def getDataWithoutUncertainError(self, outlierIndex):
        """    
        :param outlierIndex: Noise Index
        :type outlierIndex: json

        :return outlierIndex: noise index of each column
        :type: json
        """

        result = dataOutlier.getMoreNaNDataByNaNIndex(self.data, outlierIndex)
        return result

    def getOutlierIndexByMLOutlierDetector(self, outlierDetectorConfig):
        """    
        :param outlierDetectorConfig: Config for outlier detection
        :type outlierDetectorConfig: json

        :return outlierIndex: noise index of each column
        :type: json

        Example
        >>> percentile = 99
        >>> AlgorithmList =[ 'IF', 'KDE', 'LOF', 'MoG', 'SR']
        >>> algorithm = AlgorithmList[2]
        >>> config= {'algorithm': algorithm, 'percentile':percentile}#,'alg_parameter': Parameter[algorithm]
        """
        
        data_outlier = dataOutlier.DataOutlier(self.data)
        data_imputed = data_outlier.imputationForOutlierDetection()
        outlierIndex = data_outlier.getOneDetectionResult(data_imputed, outlierDetectorConfig)
 
        return outlierIndex
"""
    def removeByNeighborOutlierDetection(self, first_ratio):

        second_ratio =first_ratio + 0.1
        data_out1 = self.data.copy()
        column_list = data_out1.columns
        
        outlierIndex={}
        for column_name in column_list:
            temp = data_out1[[column_name]]
            data_1 = temp.diff().abs()
            data_2 = temp.diff(periods=2).abs()
            temp_mean = temp.mean().values[0]
            First_gap = temp_mean* first_ratio
            Second_gap = temp_mean * second_ratio
            print(First_gap, Second_gap)
            data_1_index = list(data_1[data_1[column_name] > First_gap].index)
            data_2_index = list( data_2[data_2[column_name] > Second_gap].index)
            data_1_index.extend(data_2_index)

            outlierIndex[column_name] =data_1_index
        return outlierIndex
"""
