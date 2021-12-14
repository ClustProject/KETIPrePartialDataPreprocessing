import numpy as np

def getConsecutiveNaNInfoOverThresh(data, thresh):
    # column data: data with one column
    # thresh: Threshold value to select specific ranges
    
    a = data.index
    NaNInfoOverThresh={}
    for column_name in data.columns:
        b = data[column_name].values
        idx0 = np.flatnonzero(np.r_[True, np.diff(np.isnan(b))!=0,True])
        count = np.diff(idx0)
        idx = idx0[:-1]
        valid_mask = (count>=thresh) & np.isnan(b[idx])
        out_idx = idx[valid_mask]
        out_num = a[out_idx]
        out_count = count[valid_mask]
        NaNInfoOverThresh[column_name] = list(zip(out_num, out_count))
    
    return NaNInfoOverThresh

def setNaNSpecificDuration(data, NaNInfoOverThresh, thresh):
    result = data.copy()
    for column_name in data.columns:
        for NaNInfoOverThreshitem in NaNInfoOverThresh[column_name]:
            indexLocation = data.index.get_loc(NaNInfoOverThreshitem[0])
            consecutiveNum= NaNInfoOverThreshitem[1]
            column_index = data.columns.get_loc(column_name)
            data.iloc[(indexLocation+thresh):(indexLocation+consecutiveNum), column_index] = np.nan
        result[column_name] = data[column_name]
    return data
