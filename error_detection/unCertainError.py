import numpy as np
class unCertainErrorRemove():
    '''Let UnCertain Outlier from DataFrame Data to NaN. This function makes more Nan according to the data status.
    
    **Data Preprocessing Modules**::

            neighbor_error_detected_data
    '''
    def __init__(self, data, param):
        #first_ratio=0.05
        self.data = data      
        self.param = param
    
    def get_neighbor_error_detected_data(self):
        data_out = self.data.copy()
        for feature in data_out.columns:
            test_data= data_out[[feature]].copy()
            #test_data = self.outlier_extream_value_analysis(sample_data, test_data, 10) 
            test_data= self.removeByNeighborOutlierDetection(test_data)
            data_out[[feature]] = test_data  
        
        return data_out
        
    def removeByNeighborOutlierDetection(self, data):
        first_ratio =self.param['neighbor'][0]
        second_ratio = self.param['neighbor'][1]
        column_list = data.columns
        data_out1 = data.copy()
        for column_name in column_list:
            temp = data_out1[[column_name]]
            data_1 = temp.diff().abs()
            data_2 = temp.diff(periods=2).abs()
            temp_mean = temp.mean().values[0]
            First_gap = temp_mean* first_ratio
            Second_gap = temp_mean * second_ratio
            print(First_gap, Second_gap)
            data_1_index = data_1[data_1[column_name] > First_gap].index.tolist()
            data_2_index = data_2[data_2[column_name] > Second_gap].index.tolist()

            noise_index = set(data_1_index)&set(data_2_index)
            for noise in noise_index:
                pos = data_out1.index.get_loc(noise)
                data_out1.iloc[pos].loc[column_name] = data_out1.iloc[pos-1].loc[column_name]
        return data_out1
    
    
    def outlier_extream_value_analysis(self, sample, data, extream):
        data_out= data.copy()
        for feature in data_out.columns:
            test_data = data_out[[feature]].copy()
            sample_data = sample[[feature]].copy()
            IQR = sample_data.quantile(0.75)-sample_data.quantile(0.25)
            upper_limit = sample.quantile(0.75)+(IQR*1.5)
            upper_limit_extream = sample_data.quantile(0.75)+(IQR*extream)
            lower_limit = sample_data.quantile(0.25)-(IQR*1.5)
            lower_limit_extream = sample_data.quantile(0.25)-(IQR*extream)
            test_data[(test_data < lower_limit_extream)] =np.nan
            test_data[(test_data> upper_limit_extream)] =np.nan
            
            test_data = test_data.fillna(method='ffill', limit=1)
            test_data = test_data.fillna(method='bfill', limit=1)
            data_out[[feature]] = test_data
        
        return data_out

#Hample Detection
"""
    def HampelDetection(self, data, window_size=7, n_sigma=3):
        n = len(data)
        k = 1.4826 # scale factor for Gaussian distribution
        for column in data.columns:
            data = data.reset_index(drop=True)
            for i in range((window_size),(n - window_size)):
                x0 = np.nanmedian(data[column][(i - window_size):(i + window_size)])
                S0 = k * np.nanmedian(np.abs(data[column][(i - window_size):(i + window_size)] - x0))
                if (np.abs(data[column][i] - x0) > n_sigma * S0):
                    data[column][i] = np.nan
        data.set_index('time') # 'DB time column 이름이 time인 경우'
        return data
"""

