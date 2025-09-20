from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys
import os


if __name__=="__main__":
    try:
        ingestion_obj=DataIngestion()
        print(ingestion_obj.initiate_data_ingestion())
    except Exception as e:
        raise NetworkSecurityException(e,sys)