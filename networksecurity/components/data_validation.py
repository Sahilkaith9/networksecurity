from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
import pandas as pd
import os
import sys
from networksecurity.entity.artifacts_entity import DataIngestionArtifacts,DataValidationArtifacts
from networksecurity.entity.config_entity import DataValidationConfig
from scipy.stats import ks_2samp
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_util.utils import read_yaml_file,write_yaml_file
from networksecurity.entity.config_entity import DataIngestionConfig

class DataValidation:

       def __init__(self):
            try:
                self.data_ingestion_artifacts=DataIngestionArtifacts(train_path=DataIngestionConfig().training_file_path,test_path=DataIngestionConfig().testing_file_path)
                self.data_validation_config=DataValidationConfig()
                self._schema_config=read_yaml_file(SCHEMA_FILE_PATH)
         
            
        
            except Exception as e:
                raise NetworkSecurityException(e,sys)
       def validate_number_of_columns(self,Dataframe:pd.DataFrame):
            try:
                 number_of_columns=len((self._schema_config['columns']))
                 logging.info(f"Required number of columns {number_of_columns}")
                 logging.info(f"Dataframe has columns {len(Dataframe.columns)}")
                 return number_of_columns==len(Dataframe.columns)
            except Exception as e:
                 raise NetworkSecurityException(e,sys)
            
       @staticmethod
       def read_data(file_path):
            try:
                return pd.read_csv(file_path)
            except Exception as e:
                raise NetworkSecurityException(e,sys)
   
       def detect_data_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame,threshold=0.05):
            try:
                report={}
                for column in base_df.columns:
                     d1=base_df[column]
                     d2=current_df[column]
                     is_same_dist=ks_2samp(d1,d2)
                     
                     if threshold<=is_same_dist.pvalue:
                          isFound=False
                     else :
                          isFound=True
                     
                     report[column]={
                              "p_value":float(is_same_dist.pvalue),
                              "drift_status":isFound
                         }
                    
                drift_report_file_path=self.data_validation_config.drift_report_file_path
                # file_path=os.path.dirname(drift_report_file_path)
                # os.makedirs(file_path,exist_ok=True)
                write_yaml_file(file_path=drift_report_file_path,content=report)
                return True
            except Exception as e:
                 raise NetworkSecurityException(e,sys)
     

       
       def initiate_data_validation(self):
           try:
               train_file_path=self.data_ingestion_artifacts.train_path
               test_file_path=self.data_ingestion_artifacts.test_path

               train_dataframe=DataValidation.read_data(train_file_path)
               test_dataframe=DataValidation.read_data(test_file_path)

               status=self.validate_number_of_columns(train_dataframe)
               status=self.validate_number_of_columns(test_dataframe)
               status=self.detect_data_drift(base_df=train_dataframe,current_df=test_dataframe)
               dir_name=os.path.dirname(self.data_validation_config.valid_train_file_path)
               os.makedirs(dir_name,exist_ok=True)

               train_dataframe.to_csv(self.data_validation_config.valid_train_file_path,index=False,header=True)
               train_dataframe.to_csv(self.data_validation_config.valid_test_file_path,index=False,header=True)
               
               data_validation_artifacts=DataValidationArtifacts(
                    validation_status=status,
                    valid_train_file_path=self.data_ingestion_artifacts.train_path,
                    valid_test_file_path=self.data_ingestion_artifacts.test_path,
                    invalid_train_file_path=None,
                    invalid_test_file_path=None,
                    drift_report_file_path=self.data_validation_config.drift_report_file_path

               )
               return data_validation_artifacts
           except Exception as e:
                
                raise NetworkSecurityException(e,sys)
    