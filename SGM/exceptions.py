"""Custom exceptions generated by the application"""


class NotCorrectJson(Exception):
    """Not Correct format JSON input, please check."""
    pass

class DataFrameError(Exception):
    """Сan't filter the Data, please check your DataFrame input."""
    pass