 import numpy as np
import pandas as pd

class CertainErrorRemove():
    '''Let Certain Outlier from DataFrame Data to NaN. This function makes more Nan according to the data status.
    
    **Data Preprocessing Modules**::

            Sensor Min Max Check, Remove no numeric data
    '''
    def __init__(self):
        """ Set anomal value list 
        """
        # TODO JW min_max 통과하는 모듈도 업그레이드 해야함
        # TODO anomal_value_list 외부에서 통과되도록
        # 0 은 사실 Anomaly가 아님.. ㅠㅜ
        #self.anomal_value_list = [99.9, 199.9, 299.9, 9999, -99.9, -199.9, -299.9, -9999]
        self.anomal_value_list=[99.9]

    
    def getDataWitoutcertainError(self, data, min_max_limit):
        """ Remove out-of-range errors and outliers. change error values to NaN

        :param data: input data
        :type data: DataFrame 
        :param min_max_limit: min_max_limit information
        :type min_max_limit: json

        :return: New Dataframe having more (or same) NaN
        :rtype: DataFrame

        **Two Outlier Detection Modules**::
            - remove _out_of_range_error
            - Delete Out of range error
        
        example
            >>> output = CertainErrorRemove().getDataWitoutcertainError(daata, min_max_limit)     
        """
        data_out = data.copy()
        data_out = self.remove_out_of_range_error (data_out, min_max_limit)
        data_out = self.remove_anomal_values(data_out, self.anomal_value_list)
        return data_out
        

    def remove_out_of_range_error (self, data, min_max_limit):
        """ Remove out-of-range errors. change error values to NaN

        :param data: input data
        :type data: DataFrame 
        :param min_max_limit: min_max_limit information
        :type min_max_limit: json
        
        :return: New Dataframe having more (or same) NaN
        :rtype: DataFrame
        
        example
            >>> output = CertainErrorRemove().remove_out_of_range_error(data, min_max_limit)     
        """
        data_out = data.copy()
        column_list = data.columns
        max_list = min_max_limit['max_num']
        min_list = min_max_limit['min_num']
        
        for column_name in column_list:
            if column_name in min_list.keys():
                min_num = min_list[column_name]
                mask = data_out[column_name] < min_num
                data_out.loc[mask, column_name]  = np.nan 

            if column_name in max_list.keys():
                max_num = max_list[column_name]
                mask = data_out[column_name] > max_num
                data_out.loc[mask, column_name]  = np.nan 

        return data_out

    def remove_anomal_values(self, data, anomal_value_list):
        """ Remove anomal values. change error values to NaN

        :param data: input data
        :type data: DataFrame 

        :param anomal_value_list: anomal_value_list information
        :type anomal_value_list: json
        
        :return: New Dataframe having more (or same) NaN
        :rtype: DataFrame
        
        example
            >>> output = CertainErrorRemove().remove_anomal_values(data, anomal_value_list)     
        """
        anomal_data = anomal_value_list 
        for index in anomal_data:
            data = data.replace(index, np.NaN)
        return data

class unCertainErrorRemove():
    '''Let UnCertain Outlier from DataFrame Data to NaN. This function makes more Nan according to the data status.
    
    **Data Preprocessing Modules**::

            neighbor_error_detected_data
    '''
    def __init__(self):
        pass
    
    def get_neighbor_error_detected_data(self, data, param):
        """ NaN processing for unusual outliers compared to the surrounding values.

        :param data: input data
        :type data: DataFrame 
        :param param: parameter of uncertain outlier detection
        :type param: json

        :return: New Dataframe having more (or same) NaN
        :rtype: DataFrame

        example
            >>> output = unCertainErrorRemove().get_neighbor_error_detected_data(data, param)

        """
        neighbor_param = param['neighbor']
        data_out = data.copy()
        data_out= self.error_detection_two_step_neighbor(data, neighbor_param)
        return data_out

    def error_detection_two_step_neighbor(self, data, neihbor_param):
        """ NaN processing for unusual outliers compared to the surrounding values.

        :param data: input data
        :type data: DataFrame 
        :param neihbor_param: param
        :type neihbor_param: array

        :return: New Dataframe having more (or same) NaN
        :rtype: DataFrame

        example
            >>> neighbor_param = [0.5, 0.6]
            >>> output = unCertainErrorRemove().error_detection_two_step_neighbor(data, neighbor_param)

        """
        first_ratio =neihbor_param[0]
        second_ratio = neihbor_param[1]

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
    
    """
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
    """
    