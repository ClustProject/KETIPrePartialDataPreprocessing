import numpy as np
import pandas as pd

class CertainOutlierRemove():
    # Let Certain Outlier from DataFrame Data to NaN
    # This function makes more Nan according to the data status.

    def __init__(self, data, min_max_limit):
        self.data = data
        self.min_max_limit = min_max_limit
    
    def getDataWitoutCertainOutlier(self):
        #Main Function
        # - Delete duplicated data
        # - Delete Out of range error 

        data_out = self.data.copy()
        data_out = self._out_of_range_error_remove (data_out, self.min_max_limit)
        anomal_value_list = [99.9, 199.9, 299.9, 9999, -99.9, -199.9, -299.9, -9999]
        # anomal_value_list 관련 향후 수정/업그레이드 해야 함 
        data_out = self._anomal_value_remove(data_out, anomal_value_list)
        return data_out
        

    def _out_of_range_error_remove (self, data, min_max_limit):
        data_out = data.copy()
        column_list = data.columns
        max_list = min_max_limit['max_num']
        min_list = min_max_limit['min_num']

        for column_name in column_list:
            if column_name in max_list.keys():  
                max_num = max_list[column_name]
                min_num = min_list[column_name]
                mask = data_out[column_name] > max_num
                #merged_result.loc[mask, column_name] = max_num
                data_out[column_name][mask] = np.nan#max_num
                mask = data_out[column_name] < min_num
                #merged_result.loc[mask, column_name] = min_num
                data_out[column_name][mask] = np.nan#min_num
            
        return data_out

    def _anomal_value_remove(self, data, anomal_value_list):
        # 특정 이상치 nan 처리 
        anomal_data = anomal_value_list 
        for index in anomal_data:
            data = data.replace(index, np.NaN)
        return data

#TODO Uncertain Outlier Remove 함수 에러 자주 남... 수정해야할 듯 >> 수정 완료
class UnCertainOutlierRemove():

    def __init__(self, data):
        self.data = data 
                    
    def getDataWitoutCertainOutlier(self):
        self.data_out = self.IQRDetection(self.data)
        self.data_out = self.HampelDetection(self.data)
        return self.data_out

    def IQRDetection(self, data, weight=1.5):
        # IQR을 활용한 nan 처리
        for column in data.columns:
            quantile_25 = np.percentile(data[column].values, 25)
            quantile_75 = np.percentile(data[column].values, 75)
            IQR = quantile_75 - quantile_25
            IQR_weight = IQR*weight
            lowest = quantile_25 - IQR_weight
            highest = quantile_75 + IQR_weight
            outlier_idx = data[column][(data[column] < lowest) | (data[column] > highest)].index
            data[column][outlier_idx] = np.nan
        return data

    def HampelDetection(self, data, window_size=7, n_sigma=3):
        n = len(data)
        k = 1.4826 # scale factor for Gaussian distribution
        for column in data.columns:
            data = data.reset_index()
            for i in range((window_size),(n - window_size)):
                x0 = np.nanmedian(data[column][(i - window_size):(i + window_size)])
                S0 = k * np.nanmedian(np.abs(data[column][(i - window_size):(i + window_size)] - x0))
                if (np.abs(data[column][i] - x0) > n_sigma * S0):
                    data[column][i] = np.nan
        data.set_index('time') # 'DB time column 이름이 time인 경우'
        return data