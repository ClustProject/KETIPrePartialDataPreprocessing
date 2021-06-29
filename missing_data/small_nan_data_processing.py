def simple_nan_processing(data, limit_nan_num): 

    data_non_nan= data.interpolate(method='values', limit= limit_nan_num)
    return data_non_nan

