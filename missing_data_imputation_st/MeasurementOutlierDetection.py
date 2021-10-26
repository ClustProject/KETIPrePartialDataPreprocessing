import MinMaxLimit
import numpy as np

class OutlierDetection():

    def __init__(self):
        pass

    def certain_outlier_detection(self, data, column):
        # column별 min, max 범위 밖 데이터 nan 처리
        data_min_max_limit = MinMaxLimit.MinMaxLmitValueSet().get_data_min_max_limitSet(type = 'air')
        data[data[column] > data_min_max_limit['max_num'][column]] = np.nan
        data[data[column] < data_min_max_limit['min_num'][column]] = np.nan
        return data
                    
    def uncertain_outlier_detection(self, data, column, weight=1.5):

        # 추가로 하나 더 기능 넣을 예정

        # 특정 이상치 nan 처리 
        anomal_data = [99.9, 199.9, 299.9, 9999, -99.9, -199.9, -299.9, -9999]
        for index in anomal_data:
            data = data.replace(index, np.NaN)

        # IQR을 활용한 nan 처리
        quantile_25 = np.percentile(data[column].values, 25)
        quantile_75 = np.percentile(data[column].values, 75)
        IQR = quantile_75 - quantile_25
        IQR_weight = IQR*weight
        lowest = quantile_25 - IQR_weight
        highest = quantile_75 + IQR_weight
        outlier_idx = data[column][(data[column] < lowest) | (data[column] > highest)].index
        data[data[column][outlier_idx]] = np.nan
        
        return data