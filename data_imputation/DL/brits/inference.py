
import os

class BritsInference():
    def __init__(self, data, parameter):
        self.inputData = data
        self.model_address = parameter['mode_address']
        self.get_model()

    def get_model(self):
        file_path = self.model_address
        if os.path.isfile(file_path):
            print(file_path)
        else:
            print("no_file")
            
    def get_result(self):

        return self.inputData

            