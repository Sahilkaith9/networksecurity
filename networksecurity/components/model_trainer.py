import os
import sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.utils.ml_utils.metrics.classification_metric import classification_report
from networksecurity.utils.ml_utils.model.estimator import ModelNetwork
from networksecurity.entity.artifacts_entity import DataTransformationArtifact,ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.utils.main_util.utils import load_numpy_array_data,load_object,evaluate_model,save_obj
from sklearn.linear_model import LogisticRegression
from networksecurity.components.data_transformation import DataTransformation

from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)


class ModelTrainer:
    def __init__(self):
        try:
            self.model_trainer_config=ModelTrainerConfig()
            self.data_transformation_artifacts=DataTransformation().initiate_data_transformation()
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_model_trainer(self):
        try:
            train_file_path=self.data_transformation_artifacts.transformed_train_file_path
            test_file_path=self.data_transformation_artifacts.transformed_test_file_path

            train_arr=load_numpy_array_data(train_file_path)
            test_arr=load_numpy_array_data(test_file_path)

            
            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )

            models = {
                "Random Forest": RandomForestClassifier(verbose=1),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "Logistic Regression": LogisticRegression(verbose=1),
                "AdaBoost": AdaBoostClassifier(),
            }
            params={
            
            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }
            
        }
            
            performance,trained_model= evaluate_model(x_train,y_train,x_test,y_test,models,params)

            best_model_score=max(performance.values())
            best_model_name=list(performance.keys())[list(performance.values()).index(best_model_score)]

            best_model=trained_model[best_model_name]
            save_obj(file_path=self.model_trainer_config.trained_model_file_path,object=best_model)

            # classification report --> train and test data
            y_pred_test=best_model.predict(x_test)
            report_test=classification_report(y_test,y_pred_test)

            y_pred_train=best_model.predict(x_train)
            report_train=classification_report(y_train,y_pred_train)

            model_trainer_artifacts=ModelTrainerArtifact(train_model_file_path=self.model_trainer_config.trained_model_file_path,train_metric_artifact=report_train,test_metric_artifact=report_test)
            return model_trainer_artifacts
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        