
class InvalidResponseException(Exception):
    def __init__(self, curr_index):
        super().__init__(f'Could not parse the response from index: {curr_index}')
