import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os
import sys
import numpy as np
import pickle
from sklearn.metrics import accuracy_score
from sklearn.model_selection import RandomizedSearchCV





def read_yaml_file(file_path):

    with open(file_path,'rb') as yaml_file:
        return yaml.safe_load(yaml_file) 
    


def write_yaml_file(file_path,content,replace=False):
    try:
        if replace:
            if os.path.join(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'w') as file:
            yaml.dump(content,file)

    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def save_data_object(file_path,obj):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,'wb') as file:
            np.save(file,obj)
    
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def save_obj(file_path,object):

    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,'wb') as file:
            pickle.dump(object,file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)



def load_object(file_path):
    try:
      with open(file_path,'rb') as file:
        
        return pickle.load(file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def load_numpy_array_data(file_path):
    try:
        with open(file_path,'rb') as file:
           return np.load(file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def evaluate_model(X_train,y_train,X_test,y_test,models,params):
    performance={}
    best_model={}
    try:

        for model_name,model in models.items():

            param=params[model_name]
            
            rs=RandomizedSearchCV(model,param,n_jobs=-1)
            rs.fit(X_train,y_train)

            best_model[model_name]=rs.best_estimator_
            y_test_pred=rs.predict(X_test)

            score=accuracy_score(y_test,y_test_pred)

            performance[model_name]=score
        return performance,best_model
    
    except Exception as e:
        raise NetworkSecurityException(e,sys)
