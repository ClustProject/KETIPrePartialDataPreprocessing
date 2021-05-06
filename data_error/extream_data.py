import numpy as np 
from sklearn.preprocessing import MinMaxScaler 
import pandas as pd 
import math 
import data_management.data_outlier as do

class ProcessedData():
    def __init__(self):
        pass
        
    def data_integration(self, data, resample_min):
        resample_freq = str(resample_min)+'min'
        data_key_list = list(data.keys())
        merged_data_list =[]
        data_resample={}
        for data_name in data_key_list:
            data_resample[data_name] = data[data_name].resample(resample_freq, label='left').mean()
            data_resample[data_name] = data_resample[data_name].fillna(method='bfill', limit=1)
            data_resample[data_name] = data_resample[data_name].fillna(method='ffill', limit=1)
            merged_data_list.append(data_resample[data_name])
        
        merged_data = pd.concat(merged_data_list, axis=1, join='inner')
        merged_data=merged_data.sort_index(axis=1)
       
        return merged_data
        

    def data_validation(self, data):
        data = data.loc[:, ~data.columns.duplicated()]
        first_idx = data.first_valid_index()
        last_idx = data.last_valid_index()
        valid_data = data.loc[first_idx:last_idx]
        
        return valid_data
    
    def data_cleaning(self, data_original, data_sample, data_range):
            data_key_list = list(data_original.keys())
            data_pre={}
            #feature_list={}
            for data_name in data_key_list:
                data_pre[data_name] = do.data_range_error_treatment(data_original[data_name], data_sample[data_name], data_range)

            return data_pre
    
    def data_nan_processing(self, data, resample_min, limit_minute_for_nan_processing): 
        data_key_list = list(data.keys())
        limit_num_for_nan_processing = math.ceil(limit_minute_for_nan_processing/resample_min)  
        data_non_nan= data.interpolate(method='values', limit= limit_num_for_nan_processing)
        return data_non_nan
        
    
    def data_scaling(self, data, scaler =MinMaxScaler(feature_range=(0, 1))):
         #scaling
        scaler =MinMaxScaler(feature_range=(0, 1))
        data_scale = pd.DataFrame(scaler.fit_transform(data), index=data.index,columns=data.columns)
        return scaler, data_scale

