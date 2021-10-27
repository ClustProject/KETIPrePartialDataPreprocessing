import pandas as pd 
class getData():
    def __init__(self):
        pass
    def getInfluxDB(self):
        pass
    
    def getFileInput(self, file_name, time_index="timedate"):
        dataset = pd.read_csv(file_name, parse_dates=True, index_col=[time_index])
        return dataset