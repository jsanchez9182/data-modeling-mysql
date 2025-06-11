
class InvalidResponseException(Exception):
    """ Raised when there is an attempt to handle an invalid response."""
    def __init__(self, curr_index):
        """
        Args:
            curr_index: The current index of pagination that returned an invalid response.
        """
        super().__init__(f'Could not parse the response from index: {curr_index}')
