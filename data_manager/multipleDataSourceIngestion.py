import pandas as pd 
import sys
sys.path.append("../")
sys.path.append("../..")
from KETIAppDataServer.data_manager import measurement_ingestion

class getData():
    def __init__(self):
        pass
    def getInfluxDB(self):
        pass
    
    def getFileInput(self, file_name, time_index="timedate"):
        dataset = pd.read_csv(file_name, parse_dates=True, index_col=[time_index])
        return dataset

    def getInfluxInput(self):
        from KETIPreDataIngestion.KETI_setting import influx_setting_KETI as ins
        from KETIPreDataIngestion.data_influx import influx_Client
       
        ##
        DBClient = influx_Client.influxClient(ins)
        db_list = DBClient.get_DBList()
        db_name  = 'air_indoor_경로당'
        ms_list = DBClient.measurement_list(db_name)
        ms_name = ms_list[0]

        feature_list = DBClient.get_fieldList(db_name, ms_name)
        full_data = DBClient.get_data(db_name, ms_name)

        # 우선 full data 가져오도록 해놨음 db 이름과 ms 이름은 list에서 적당한것 바꿔볼 수 있음
        return full_data
