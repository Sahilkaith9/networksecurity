import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os
import sys
import numpy as np
import pickle





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
