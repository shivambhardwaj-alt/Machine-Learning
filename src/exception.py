import sys
from src.logger import logging

def error_message_detail(error,detail:sys) :
    _,_,exc_tb = detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    error_message = f"Error occurred in script: {file_name} at line number: {line_number} with message: {str(error)}"
    return error_message

class CustomException(Exception):
    """A custom exception class that extends the built-in Exception class."""

    def __init__(self, message):
        super().__init__(message)
        self.message = error_message_detail(message, sys)

    def __str__(self):
        return f"CustomException: {self.message}"
def raise_custom_exception(message):
    """Function to raise a CustomException with the given message."""
    raise CustomException(message)
if __name__ == "__main__":
    try:
        raise_custom_exception("This is a custom error message.")
    except CustomException as e:
        print(e)
        sys.exit(1)
