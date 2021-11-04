def duplicate_data_remove(data):
    
    # duplicated column remove
    data = data.loc[:, ~data.columns.duplicated()]
    # duplicated Index Drop
    data = data.sort_index()
    # duplicated index remove
    """
    first_idx = data.first_valid_index()
    last_idx = data.last_valid_index()
    valid_data = data.loc[first_idx:last_idx]
    # 
    """
    valid_data = data[~data.index.duplicated(keep='first')]
    ####
        
    return valid_data

def make_static_frequency(data):
    # This function make static frequency 
    data_staticFrequency = data.copy()
    if len(data)> 3:
        #inferred_freq = pd.infer_freq(data_partial_raw[:5])
        inferred_freq1 = (data.index[1]-data.index[0])
        inferred_freq2 = (data.index[2]-data.index[1])
        # Simply compare 2 intervals from 3 data points.
        # If this data has a static frequency from 3 data points, make the static description time-indexed data
        if inferred_freq1 == inferred_freq2:
            data_staticFrequency = data.asfreq(freq=inferred_freq1)

    return data_staticFrequency