import sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from sklearn.model_selection import train_test_split
import os
import pymongo
from networksecurity.entity.config_entity import DataIngestionConfig
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from networksecurity.entity import artifacts_entity
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")


class DataIngestion:
    def __init__(self):
        self.data_ingestion_config=DataIngestionConfig()
    
    def export_collection_as_datafroma(self):
       try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            collection=self.mongo_client[database_name][collection_name]
            df=pd.DataFrame(list(collection.find()))

            if "_id" in df.columns:
                df.drop('_id',axis=1,inplace=True)
            df.replace({"na":np.nan},inplace=True)
            return df
       except Exception as e:
           raise NetworkSecurityException(e,sys)

    def initiate_data_ingestion(self):
        try:
            dataframe=self.export_collection_as_datafroma()
            os.makedirs(os.path.dirname(self.data_ingestion_config.feature_store_file_path),exist_ok=True)
            dataframe.to_csv(self.data_ingestion_config.feature_store_file_path,index=False,header=True)

            train_set,test_set=train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio,random_state=42)

            os.makedirs(os.path.dirname(self.data_ingestion_config.training_file_path),exist_ok=True)
            os.makedirs(os.path.dirname(self.data_ingestion_config.testing_file_path),exist_ok=True)

            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)



            ingestionArtifact= artifacts_entity.DataIngestionArtifacts(train_path=self.data_ingestion_config.training_file_path,test_path=self.data_ingestion_config.testing_file_path)
            return ingestionArtifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    