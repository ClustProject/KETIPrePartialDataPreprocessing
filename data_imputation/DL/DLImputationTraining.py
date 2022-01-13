import os
import sys
import torch
sys.path.append(".")
sys.path.append("..")
sys.path.append("../..")
sys.path.append("../../..")
sys.path.append("../../../..")

from KETIPrePartialDataPreprocessing.data_imputation.DL.brits import training

class ImputationTraining():
    def __init__(self, dbClient, rootDir):
        self.DBClient = dbClient
        self.root_dir = rootDir

    def trainerForDB(self, db_name, bind_params):
        self.db_name = db_name
        self.MSList = self.DBClient.measurement_list(self.db_name)
        for ms_name in self.MSList:
            self.trainerForMS(db_name, ms_name, bind_params)

    def trainerForMS(self, db_name, ms_name, bind_params):
        df = self.DBClient.get_data_by_time(bind_params, db_name, ms_name)
        for column_name in df.columns:
            column_data = df[[column_name]]
            model_name = self.trainSaveModel(column_data, column_name)
            print(model_name, " saved")

    def trainSaveModel(self, df, df_name): 
        self.model_folder = os.path.join(self.root_dir, db_name, ms_name) 

        if not os.path.exists(self.model_folder):
            os.makedirs(self.model_folder) 

        self.model_addr = os.path.join(self.root_dir, db_name, ms_name, df_name)
        model_name = self.model_addr + '.pth'
        json_name = self.model_addr  + '.json'

        T = training.britsImputationTraining(df, json_name)
        model = T.columnDataTrainer()
        torch.save(model.state_dict(), model_name)
        return model_name
         
        


if __name__ == '__main__':
    #print(sys.path)
    from KETIPreDataIngestion.KETI_setting import influx_setting_KETI as ins
    from KETIPreDataIngestion.data_influx import influx_Client

    DBClient = influx_Client.influxClient(ins.CLUSTDataServer)
    
    # Example 1 
    # db_name = 'air_indoor_경로당'
    # ms_name = 'ICL1L2000234'
    db_name = 'air_indoor_요양원'
    ms_name = 'ICL1L2000017'
    first = DBClient.get_first_time(db_name, ms_name)
    last = DBClient.get_last_time(db_name, ms_name)
    print(first, last)
    
    first ='2020-06-18'
    last ='2020-06-19'

    rootDir = os.path.join(os.getcwd(), 'data_imputation', 'DL', 'brits', 'model')
    bind_params = {'end_time':last, 'start_time': first}

    mode_list = ['MS_Training', 'DB_Training']
    mode = mode_list[0] ## mode select
    imT = ImputationTraining(DBClient, rootDir)
    if mode == 'MS_Training':
        ## train for Measurment
        imT.trainerForMS(db_name, ms_name, bind_params)
    elif mode == 'DB_Training':
        ## train for Database
        imT.trainerForDB(db_name, bind_params)
    