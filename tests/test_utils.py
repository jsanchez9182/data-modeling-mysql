import pytest
from pathlib import PosixPath
from bookmodeling.exceptions import MissingDirectoriesException
from bookmodeling.utils import get_latest_dir


class TestGetLatestDate:
    def test_valid_directory(self, raw_data_sample):
        adventure_dir = raw_data_sample / 'adventure'

        assert get_latest_dir(adventure_dir) == PosixPath('2025-06-21')

    def test_empty_directory(self, raw_data_sample, caplog):
        historic_dir = raw_data_sample / 'historic'
        with pytest.raises(MissingDirectoriesException):
            get_latest_dir(historic_dir)

        assert caplog.records[0].msg == 'No directories in historic directory.'