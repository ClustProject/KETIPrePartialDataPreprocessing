
def duplicate_data_remove(data):
    # duplicated Column, Index Drop
    data = data.sort_index()
    data = data.loc[:, ~data.columns.duplicated()]
    first_idx = data.first_valid_index()
    last_idx = data.last_valid_index()
    valid_data = data.loc[first_idx:last_idx]
    valid_data = valid_data.drop_duplicates(keep='first')
        
    return valid_data

def make_static_frequency(data):
    # This function make static frequency 
    data_staticFrequency = data.copy()
    if len(data)> 2:
        #inferred_freq = pd.infer_freq(data_partial_raw[:5])
        inferred_freq = (data.index[1]-data.index[0])
        data_staticFrequency = data.asfreq(freq=inferred_freq)
    return data_staticFrequency