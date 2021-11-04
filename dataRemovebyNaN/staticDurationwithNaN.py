import pandas as pd
def makeFullStartEndTimeDatawithNaN(data, start, end, freq):
    data.index = data.index.tz_localize(None)
    new_idx = pd.date_range(start = start, end = end, freq = freq)
    new_data = pd.DataFrame(index= new_idx)
    new_data.index.name ='time' 
    data = new_data.join(data) 
    return data