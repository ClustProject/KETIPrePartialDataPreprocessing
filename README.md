
# KETIPrePartialDataPreprocessing
> Preprocessing module for one single dataset. 

It includes cleaning, imputation, outlier detection modules.
And It also has dataRemoveByNaN module which remove a part of data according to the NaN status.

## makeNaNImputationTest.py (+ makeNaNImputationTest.ipynb)
> This is the code to test the data_preprocessing module 
> Input can be both file or inlxlufDB 
(If you want to change db and measurement name, you need to modify multipleDataSourceIngestion.py)

## data_preprocessing.py
> data_preprocessing.get_preprocessed_data(input_data, refine_param, outlier_param, imputation_param)
- This function get data through all possible data preprocessing module.
- So far, data refining, outlier removal, imputation module are available.
We have a plan to extend more preprocessing modules.
