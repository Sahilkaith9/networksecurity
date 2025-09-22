from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys
from networksecurity.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME


class ModelNetwork:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor=preprocessor
            self.model=model
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def predict(self,x):
       try:
            x_transformed=self.preprocessor.transform(x)
            y_hat=self.model.predict(x_transformed)
            return y_hat
       except Exception as e :
           raise NetworkSecurityException(e,sys)