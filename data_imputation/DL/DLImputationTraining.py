import os
import sys
import torch
sys.path.append(".")
sys.path.append("..")
sys.path.append("../..")
sys.path.append("../../..")
sys.path.append("../../../..")

from KETIToolDL.Imputation.brits import training
from KETIToolDL.InfluxDB import InfluxDBTraining as IDT

class BritsInfluxTraining(IDT.InfluxDBTraining):
    def setModelFileName(self, target_name):
        self.model_name = target_name + '.pth'
        self.json_name = target_name  + '.json'
        self.model_path =os.path.join(self.model_folder, self.model_name)
        self.json_path = os.path.join(self.model_folder, self.json_name)

    def trainSaveModel(self, df): 
        Brits = training.BritsTraining(df, self.json_path)
        model = Brits.train()
        torch.save(model.state_dict(), self.model_path)
        print(self.model_path)

def trainInfluxData(model_method, mode):
    if model_method == 'brits':
        trainer = BritsInfluxTraining(DBClient, rootDir)
    if mode == 'MS_Training':
        ## train for Measurment
        trainer.trainerForMS(db_name, ms_name, bind_params)
    
    elif mode == 'DB_Training':
        ## train for Database
        trainer.trainerForDB(db_name, bind_params)

if __name__ == '__main__':
    #print(sys.path)
    from KETIPreDataIngestion.KETI_setting import influx_setting_KETI as ins
    from KETIPreDataIngestion.data_influx import influx_Client
    
    ##########################################
    mode_list = ['MS_Training', 'DB_Training']
    model_method_list = ['brits']
    model_purpose_list=['imputation']
    ##########################################
    DBClient = influx_Client.influxClient(ins.CLUSTDataServer)
    db_name = 'air_indoor_요양원'
    ms_name = 'ICL1L2000017'
    #first = DBClient.get_first_time(db_name, ms_name)
    #last = DBClient.get_last_time(db_name, ms_name)
    first ='2020-06-18'
    last ='2020-06-19'
    ##########################################
    bind_params = {'end_time':last, 'start_time': first}
    mode = mode_list[0] ## mode select
    model_purpose = model_purpose_list[0]
    model_method = model_method_list[0]
    rootDir = os.path.join('Users', 'bunnyjw','Git', 'DL', 'Models', model_purpose, model_method)
    ###########################################

    trainInfluxData(model_method, mode)