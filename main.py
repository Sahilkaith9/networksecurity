from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys
import os
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation


if __name__=="__main__":
    try:
        ingestion_obj=DataIngestion()
        print(ingestion_obj.initiate_data_ingestion())
        validate_obj=DataValidation()
        validate_obj.initiate_data_validation()
        data_transformation=DataTransformation()
        data_transformation.initiate_data_transformation()
    except Exception as e:
        raise NetworkSecurityException(e,sys)