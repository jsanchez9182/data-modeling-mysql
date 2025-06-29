
class InvalidResponseException(Exception):
    """ Raised when there is an attempt to handle an invalid response."""
    def __init__(self, curr_index):
        """
        Args:
            curr_index: The current index of pagination that returned an invalid response.
        """
        super().__init__(f'Could not parse the response from index: {curr_index}')


class ValidationPercentException(Exception):
    def __init__(self, msg):
        """
        Raised if minimum percent of valid records is not reached.
        """
        super().__init__(msg)


class MissingDataException(Exception):
    def __init__(self):
        """
            Raised when there is no data to validate.
        """
        super().__init__("No records pulled from the files.")

class MissingDirectoriesException(Exception):
    """
        Raised when there are no date directories in the keyword directory.
    """
    def __init__(self, keyword_dir: str):
        super().__init__(f"No directories in the {keyword_dir} directory.")

class MissingFilesException(Exception):
    """
        Raised when there are no data files in the latest date directory in the keyword directory.
    """
    def __init__(self, latest_dir: str):
        super().__init__(f"No data files in the {latest_dir} directory.")