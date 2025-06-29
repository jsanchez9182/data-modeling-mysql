import logging
import pytest
from pathlib import PosixPath
from unittest.mock import Mock, call
import bookmodeling.api_request
from bookmodeling.api_request import search_google_keywords
from bookmodeling.exceptions import InvalidResponseException
from tests.conftest import ValidMockResponse



class TestGoogleBooksClient:
    def test_get_output_path(self, client, tmp_path):
        assert client.get_output_path() == tmp_path / PosixPath(f'raw_data/flowers/2025-07-05/start_index_0.json')

    def test_pull_data(self, client, monkeypatch, tmp_path, caplog):
        caplog.set_level(logging.INFO)
        first_output_path = tmp_path / PosixPath(f'raw_data/flowers/2025-07-05/start_index_0.json')

        # An error should be raised when processing second response
        with pytest.raises(InvalidResponseException):
            client.pull_data()

        # First response should write to the tmp_output_path and generate a success log message.
        with open(first_output_path, 'r') as f:
            assert f.read() == ValidMockResponse().text
        assert caplog.records[0].message == (f'keyword: flowers, start_index: 0,'
                        f' max_results: 2, Status code: 200')

        # Second response should generate a failure log message.
        assert caplog.records[1].message == (f'keyword: flowers, start_index: 1, max_results: 2,'
                        f' Status code: 500, Reason: No data.')


def test_search_keywords(monkeypatch):
    """
    Checking that GoogleBooksClient is instantiated with correct args and
    that pull_data method is called after.
    """
    mock = Mock()
    monkeypatch.setattr(bookmodeling.api_request, 'GoogleBooksClient', mock)

    search_google_keywords(['adventure', 'haunted'], 2, 5, 'raw_data')
    calls = [call('adventure', 0, 2, 5, 'raw_data'), call().pull_data(),
             call('haunted', 0, 2, 5, 'raw_data'), call().pull_data()]

    mock.assert_has_calls(calls)