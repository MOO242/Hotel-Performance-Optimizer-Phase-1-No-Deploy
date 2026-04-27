import sys


def format_error_message(error: Exception) -> str:
    """
    Extracts detailed error information including:
    - file name
    - line number
    - error message
    """

    _, _, exc_tb = sys.exc_info()

    if exc_tb is None:
        return str(error)

    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    error_message = (
        f"Error occurred in script: {file_name} "
        f"at line: {line_number} "
        f"with message: {str(error)}"
    )

    return error_message


class CustomException(Exception):
    """
    Custom exception class that formats errors with file name and line number.
    """

    def __init__(self, error: Exception):
        super().__init__(str(error))
        self.error_message = format_error_message(error)

    def __str__(self):
        return self.error_message
