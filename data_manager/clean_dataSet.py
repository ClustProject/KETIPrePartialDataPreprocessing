from KETIPrePartialDataPreprocessing.PartialDataCleansing.definite_error_detection import valid_data, outlier_detection

def make_clean_dataSet(data_original, func, argument='None'):
    data_clean={}
    for i, data in enumerate(data_original):
        #data_sample = data_original[i][:100]
        data = data_original[i]
        if argument == 'None':
            data_clean[i] = func(data)
        else:
            data_clean[i] = func(data, argument)
        
    return data_clean

class cleanDataSet():
    def __init__(self, data_partial_raw, limit_min_max):
        self.limit_min_max = limit_min_max
        self.data_partial_raw = data_partial_raw
        self.data_partial_clean={}
        self.limit_nan_num = 10
    
    def get_clean_partial_dataset(self):
       
        # 3-1. Get the valid data within a specific range  
        self.data_partial_clean[0] = make_clean_dataSet(self.data_partial_raw, valid_data.ValidData().get_valid_data, self.limit_min_max)
        # 4. Get the data without extream outlier
        self.data_partial_clean[1]= make_clean_dataSet(self.data_partial_clean[0], outlier_detection.OutlierDetection().get_neighbor_error_detected_data)
        # 5. 
        from KETIPrePartialDataPreprocessing.PartialDataCleansing.definite_error_detection import small_nan_data_processing 
        
        self.data_partial_clean[2]= make_clean_dataSet(self.data_partial_clean[1], small_nan_data_processing.simple_nan_processing, self.limit_nan_num)

        return self.data_partial_clean[2]