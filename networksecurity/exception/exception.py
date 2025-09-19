import sys


class NetworkSecurityException(Exception):
    def __init__(self,error_message,error_details:sys):
        super().__init__(error_message)
        self.error_message=error_message
        _,_,exc_tb=error_details.exc_info()

        self.filename=exc_tb.tb_frame.f_code.co_filename
        self.linenumber=exc_tb.tb_lineno
    
    def __str__(self):
        return f"Error occured in script {self.filename} in the line number {self.linenumber} with message {self.error_message}"