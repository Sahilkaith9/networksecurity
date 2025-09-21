from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys
import os
from networksecurity.components.data_validation import DataValidation


if __name__=="__main__":
    try:
        ingestion_obj=DataIngestion()
        print(ingestion_obj.initiate_data_ingestion())
        validate_obj=DataValidation()
        validate_obj.initiate_data_validation()
    except Exception as e:
        raise NetworkSecurityException(e,sys)