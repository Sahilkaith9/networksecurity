import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os
import sys






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