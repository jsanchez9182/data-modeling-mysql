import requests
import logging
import time
from datetime import date
import os
from bookmodeling.exceptions import InvalidResponseException

logger = logging.getLogger(__name__)

class BookRequest:
    def __init__(self, keyword: str, start_index: int, end_index: int, max_results: int):
        self.keyword = keyword
        self.start_index = start_index
        self.end_index = end_index
        self.max_results = max_results

    def get_response(self):
        params = {
            'q': self.keyword,
            'intitle': self.keyword,
            'start_index': self.start_index,
            'max_results': self.max_results
        }
        return requests.get('https://www.googleapis.com/books/v1/volumes', params)

    def get_output_path(self):
        return f'raw_data/{self.keyword}/{date.today().isoformat()}/start_index_{self.start_index}.json'

    def handle_response(self, response: requests.Response) -> None:
        if response.status_code == 200:
            file_path = self.get_output_path()
            # Create necessary output directories if they do not exist.
            dir_path = os.path.dirname(file_path)
            os.makedirs(dir_path, exist_ok=True)

            logger.info(f'keyword: {self.keyword}, start_index: {self.start_index},'
                        f' max_results: {self.max_results}, Status code: {response.status_code}')

            with open(file_path, 'w') as f:
                f.write(response.text)

        else:
            logger.info(f'keyword: {self.keyword}, start_index: {self.start_index}, max_results: {self.max_results},'
                        f' Status code: {response.status_code}, Reason: {response.reason}')

            raise InvalidResponseException(self.start_index)

    def get_data(self) -> None:
        for _ in range(self.start_index, self.end_index):
            response = self.get_response()
            self.handle_response(response)
            self.start_index += 1
            # Google Books Api rate limit 100 requests in 60 seconds.
            time.sleep(0.6)
