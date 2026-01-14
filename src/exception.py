import sys
from .logger import logging


def error_message_detail(error, error_detail):
    """
    Returns a detailed error message with file name and line number.
    """
    _, _, exc_tb = error_detail.exc_info()

    
    if exc_tb is None:
        return str(error)

    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno

    error_message = (
        f"Error occurred in script: {file_name} "
        f"at line number: {line_number} "
        f"with message: {str(error)}"
    )

    logging.error(error_message)
    return error_message


class CustomException(Exception):
    def __init__(self, error, error_detail=sys):
        """
        Custom exception that logs detailed error information.
        """
        super().__init__(error)
        self.error_message = error_message_detail(error, error_detail)

    def __str__(self):
        return self.error_message




