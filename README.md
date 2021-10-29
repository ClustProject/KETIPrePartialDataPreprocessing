
# KETIPrePartialDataPreprocessing
> Preprocessing module for one single dataset. 

It includes cleaning, imputation, outlier detection modules.
And It also has dataRemoveByNaN module which remove a part of data according to the NaN status.

## 1. makeNaNImputationTest.py (+ makeNaNImputationTest.ipynb)
> This is the code to test the data_preprocessing module 
> Input can be both file or inlxlufDB 
(If you want to change db and measurement name, you need to modify multipleDataSourceIngestion.py)

## 2. data_preprocessing.py
### 2-1. function get_preprocessed_data(input_data, refine_param, outlier_param, imputation_param)
> This function gets cleaner data by all possible data preprocessing modules from KETIPrePartialDataPreprocessing packages.

### 2-2. DataPreprocessing (class)
> This class provdies several preprocessing Method from this package.

- So far, data refining, outlier removal, imputation module are available.
- There is a plan to expand more preprocessing modules.
