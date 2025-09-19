import os
import sys
import json
import certifi
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import pymongo
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
load_dotenv()

MONGO_DB_URL=os.getenv('MONGO_DB_URL')
print(MONGO_DB_URL)

ca=certifi.where()



class NetworkSecurityExtract:
    
    def csv_to_json_converter(self,file_path):
        try:
            data=pd.read_csv(file_path)
            
            records=list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def insert_data_mongodb(self,record,database,collection):
        try:
            self.record=record
            self.database=database
            self.collection=collection
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
           
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]

           
            
            self.collection.insert_many(self.record)
            return len(self.record)
        except Exception as e :
            raise NetworkSecurityException(e,sys)

if __name__=='__main__':
    FILE_PATH='Network_Data/phisingData.csv'
    DATABASE="SAHILAI"
    Collection="NetworkData"
    network_obj=NetworkSecurityExtract()
    records=network_obj.csv_to_json_converter(FILE_PATH)
    no_of_records=network_obj.insert_data_mongodb(records,DATABASE,Collection)
    print(no_of_records)