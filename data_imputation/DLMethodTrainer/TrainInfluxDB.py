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

def trainInfluxData(model_method, mode, DBClient, db_name, ms_name, bind_params, model_root_dir):
    if model_method == 'brits':
        trainer = BritsInfluxTraining(DBClient, model_root_dir)
        
    if mode == 'MS_Training':
        ## train for Measurment
        trainer.trainerForMS(db_name, ms_name, bind_params)
    
    elif mode == 'DB_Training':
        ## train for Database
        trainer.trainerForDB(db_name, bind_params)
