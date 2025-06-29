from pathlib import Path
import requests
import logging
import time
from datetime import date
from bookmodeling.exceptions import InvalidResponseException

logger = logging.getLogger(__name__)

class GoogleBooksClient:
    """
    Client used to make requests to the Google Books API.
    """
    def __init__(self, keyword: str, start_index: int, end_index: int, max_results: int, output_dir: str):
        """
        Args:
            keyword: Keyword to search in titles.
            start_index: Start index (of pagination)
            end_index: End index of pagination (not inclusive)
            max_results: Results included on each request.
            output_dir: The directory where raw data will be stored.
        """
        self._keyword = keyword
        self._start_index = start_index
        self._end_index = end_index
        self._max_results = max_results
        self._output_dir = output_dir

    def _get_response(self) -> requests.Response:
        # Returns response from Google Books API
        params = {
            'q': self._keyword,
            'intitle': self._keyword,
            'start_index': self._start_index,
            'max_results': self._max_results
        }
        return requests.get('https://www.googleapis.com/books/v1/volumes', params)

    def get_output_path(self) -> Path:
        """
        Returns: Path with output destination.
        """
        return Path(f'{self._output_dir}/{self._keyword}/{date.today().isoformat()}/start_index_{self._start_index}.json')


    def _handle_response(self, response: requests.Response) -> None:
        # Writes successful responses to file_path. Raises InvalidResponseException otherwise.
        if response.status_code == 200:
            file_path = self.get_output_path()

            logger.info(f'keyword: {self._keyword}, start_index: {self._start_index},'
                        f' max_results: {self._max_results}, Status code: {response.status_code}')

            # Create necessary output directories if they do not exist.
            file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, 'w') as f:
                f.write(response.text)
        else:
            logger.error(f'keyword: {self._keyword}, start_index: {self._start_index}, max_results: {self._max_results},'
                        f' Status code: {response.status_code}, Reason: {response.reason}')

            raise InvalidResponseException(self._start_index)

    def pull_data(self) -> None:
        """
        Iterates from start_index to end_index and writes responses to dedicated file paths.
        Terminates on unsuccessful requests.

        Returns: None
        """
        for _ in range(self._start_index, self._end_index):
            response = self._get_response()
            self._handle_response(response)
            self._start_index += 1
            # Google Books API rate limit 100 requests in 60 seconds.
            time.sleep(0.6)

def search_google_keywords(keywords: list[str], end_index: int,  max_results: int, output_dir: str) -> None:
    """
    Generates GoogleBooksClient and pulls data for each keyword.

    Args:
        keywords: List of keywords to search.
        end_index: Page to stop search (not inclusive).
        max_results: Results displayed on each request.

    Returns: None

    """
    for keyword in keywords:
        client = GoogleBooksClient(keyword, 0, end_index, max_results, output_dir)
        client.pull_data()
