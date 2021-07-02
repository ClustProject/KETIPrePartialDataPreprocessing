#data_resample[data_name] = data_resample[data_name].fillna(method='bfill', limit=1)
#data_resample[data_name] = data_resample[data_name].fillna(method='ffill', limit=1)
        
class OutlierDetection():
    def __init__(self):
        #first_ratio=0.05
        self.first_ratio = 0.5
        self.second_ratio = 0.5
        pass
    
    def get_neighbor_error_detected_data(self, data):
        data_out = data.copy()
        sample  = data_out[:60]
        for feature in data_out.columns:
            test_data= data_out[[feature]].copy()
            sample_data = sample[[feature]].copy()
            # test_data = outlier_extream_value_analysis(sample_data, test_data, 10) (나중에 수정해서 필요시 사용해야 함)
            test_data= self.outlier_detection_two_step_neighbor(sample_data, test_data)
            data_out[[feature]] = test_data  
        
        return data_out

    def outlier_detection_two_step_neighbor(self, sample, data):
        column_list = data.columns
        data_out1 = data.copy()
        for column_name in column_list:
            temp = data_out1[[column_name]]
            sample_temp = sample[[column_name]]
            data_1 = temp.diff().abs()
            data_2 = temp.diff(periods=2).abs()
            temp_mean = sample_temp.mean().values[0]
            First_gap = temp_mean* self.first_ratio
            Second_gap = temp_mean * self.second_ratio
            data_1_index = data_1[data_1[column_name] > First_gap].index.tolist()
            data_2_index = data_2[data_2[column_name] < Second_gap].index.tolist()
            noise_index = set(data_1_index)&set(data_2_index)
    
            for noise in noise_index:
                pos = data_out1.index.get_loc(noise)
                data_out1.iloc[pos-1].loc[column_name] = data_out1.iloc[pos].loc[column_name]
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

