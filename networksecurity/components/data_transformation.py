import os
import sys
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.entity.artifacts_entity import DataTransformationArtifact,DataValidationArtifacts
from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.utils.main_util.utils import save_data_object,save_obj
from networksecurity.components.data_validation import DataValidation
import pandas as pd


class DataTransformation:
    def __init__(self):
        try:
            self.data_validation_artifacts=DataValidation().initiate_data_validation()
            self.data_transformation_config=DataTransformationConfig()
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    @staticmethod
    def get_data(file_path):
        try:
           return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def get_data_transformer(self):
        try:
            preprocessor=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            pipeline=Pipeline(
                [("imputer",preprocessor)]
            )
            return pipeline
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_transformation(self):
        try:
            train_df=DataTransformation.get_data(self.data_validation_artifacts.valid_train_file_path)
            test_df=DataTransformation.get_data(self.data_validation_artifacts.valid_test_file_path)

            # splitting the dataset in test and train
            input_features_train_data=train_df.drop(TARGET_COLUMN,axis=1)
            target_feature_train_data=train_df[TARGET_COLUMN]

            input_features_test_data=test_df.drop(TARGET_COLUMN,axis=1)
            target_feature_test_data=test_df[TARGET_COLUMN]

            preprocessor=self.get_data_transformer()
            transformed_input_features_train_data=preprocessor.fit_transform(input_features_train_data)
            transformed_input_features_test_data=preprocessor.transform(input_features_test_data)

            train_arr=np.c_[transformed_input_features_train_data,np.array(target_feature_train_data)]
            test_arr=np.c_[transformed_input_features_test_data,np.array(target_feature_test_data)]

            save_data_object(file_path=self.data_transformation_config.transformed_train_file_path,obj=train_arr)
            save_data_object(file_path=self.data_transformation_config.transformed_test_file_path,obj=test_arr)
            save_obj(file_path=self.data_transformation_config.transformed_object_file_path,object=preprocessor)

            data_transformation_artifacts= DataTransformationArtifact(
               transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
               transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
               transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
           )
            return  data_transformation_artifacts

        except Exception as e:
            raise NetworkSecurityException(e,sys)
