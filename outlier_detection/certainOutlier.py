
import numpy as np
import pandas as pd

class CertainOutlierRemove():
    '''Let Certain Outlier from DataFrame Data to NaN. This function makes more Nan according to the data status.
    
    **Data Preprocessing Modules**::

            ``Sensor Min Max Check``, ``Remove no numeric data``
    '''
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
        # TODO JW anomal_value_list 관련 향후 수정/업그레이드 해야 함 
        data_out = self._anomal_value_remove(data_out, anomal_value_list)
        return data_out
        

    def _out_of_range_error_remove (self, data, min_max_limit):
        data_out = data.copy()
        column_list = data.columns
        max_list = min_max_limit['max_num']
        min_list = min_max_limit['min_num']
        
        for column_name in column_list:
            if column_name in min_list.keys():
                min_num = min_list[column_name]
                mask = data_out[column_name] < min_num
                #merged_result.loc[mask, column_name] = min_num
                data_out[column_name][mask] = np.nan #min_num

            if column_name in max_list.keys():
                max_num = max_list[column_name]
                mask = data_out[column_name] > max_num
                data_out[column_name][mask] = np.nan #max_num

        return data_out

    def _anomal_value_remove(self, data, anomal_value_list):
        # 특정 이상치 nan 처리 
        anomal_data = anomal_value_list 
        for index in anomal_data:
            data = data.replace(index, np.NaN)
        return data