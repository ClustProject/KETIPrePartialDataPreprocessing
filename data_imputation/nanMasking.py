import numpy as np

def getConsecutiveNaNInfoOverThresh(data, column_name, thresh):
    # column data: data with one column
    # thresh: Threshold value to select specific ranges
    
    a = data.index
    b = data[column_name].values
    idx0 = np.flatnonzero(np.r_[True, np.diff(np.isnan(b))!=0,True])
    count = np.diff(idx0)
    idx = idx0[:-1]
    valid_mask = (count>=thresh) & np.isnan(b[idx])
    out_idx = idx[valid_mask]
    out_num = a[out_idx]
    out_count = count[valid_mask]
    out = zip(out_num, out_count)
    return out

def setNaNSpecificDuration(data, column_name, NaNInfoOverThresh, thresh):
    for NaNInfoOverThreshitem in NaNInfoOverThresh:
        indexLocation = data.index.get_loc(NaNInfoOverThreshitem[0])
        consecutiveNum= NaNInfoOverThreshitem[1]
        column_index = data.columns.get_loc(column_name)
        data.iloc[(indexLocation+thresh):(indexLocation+consecutiveNum), column_index] = np.nan
    return data
