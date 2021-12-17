import os
class ImputationTraining():
    def __init__(self, dbClient, rootDir):
        self.DBClient =dbClient
        self.rootDir = rootDir

    def traininerForDB(self, db_name, bind_param):
        self.db_name = db_name
        self.MSList = self.DBClient.measurement_list(self.db_name)
        for ms_name in self.MSList:
            self.trainerForMS(db_name, ms_name, bind_param)

    def trainerForMS(self, db_name, ms_name, bind_params):
        df = self.DBClient.get_data_by_time(bind_params, db_name, ms_name)
        for column_name in df.columns:
            column_data = df[[column_name]]
            model = self.columnDataTrainer(column_data)
            model_name = self.getModelAdd(db_name, ms_name, column_name)
            self.model_store(model_name, model)

    def getModelAdd(self, db_name, ms_name, column_name):
        model_name = os.path.add(self.root_dir, db_name, ms_name, column_name,'dfdf')
        return model_name

    def model_store(self, model_name, model):
        pass

    def columnDataTrainer(self,colum_data):
        pass

class britsImputationTraining(ImputationTraining):
    def columnDataTraininer()


if __name__ == '__main__':
    from KETIPreDataIngestion.KETI_setting import influx_setting_KETI as ins
    from KETIPreDataIngestion.data_influx import influx_Client

    DBClient = influx_Client.influxClient(ins)
    imT = ImputationTraining(DBClient)
    bind_params = {'end_time':query_end_time, 'start_time': query_start_time}
    db_name="dfdf"
    #imT.trainerForDB(db_name, bind_params)
    imT.trainForMS)
