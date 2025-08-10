import pytest

from bookmodeling.exceptions import MissingFilesException, MissingDataException, ValidationPercentException
from bookmodeling.validators import ValidationManager


@pytest.fixture
def validation_manager(tmp_path, request):
    input_dir = tmp_path / 'raw_data_sample'
    output_dir = tmp_path / 'validated_data'
    keyword = request.param

    return ValidationManager(str(input_dir), str(output_dir), keyword, 70)


class TestValidationManager:

    @pytest.mark.parametrize('validation_manager', ['romantic'], indirect=True)
    def test_run_validation_empty_latest_dir(self, raw_data_sample, validation_manager, caplog):
        with pytest.raises(MissingFilesException):
            validation_manager.run_validation()

        assert caplog.records[0].msg == 'No files in the romantic/2025-06-24 directory.'

    @pytest.mark.parametrize('validation_manager', ['exciting'], indirect=True)
    def test_run_validation_no_data(self, raw_data_sample, validation_manager, caplog):
        with pytest.raises(MissingDataException):
            validation_manager.run_validation()

        assert caplog.records[0].msg == 'No records in the directory.'

    @pytest.mark.parametrize('validation_manager', ['haunted'], indirect=True)
    def test_run_validation_below_std_data(self, raw_data_sample, validation_manager, caplog):
        with pytest.raises(ValidationPercentException):
            validation_manager.run_validation()

        assert caplog.records[0].msg == "Msg: Field required, Loc: ('id',)"
        assert caplog.records[1].msg == "Msg: Field required, Loc: ('volumeInfo', 'title')"
        assert caplog.records[2].msg == "Msg: Field required, Loc: ('volumeInfo',)"
        assert caplog.records[3].msg == "Msg: Field required, Loc: ('id',)"
        assert caplog.records[4].msg == 'Excepted 70.0 percent of records to pass validation but only 60.0 passed.'

    @pytest.mark.parametrize('validation_manager', ['scary'], indirect=True)
    def test_run_validation(self, raw_data_sample, validation_manager, tmp_path, validated_data):
        output_file = tmp_path / 'validated_data/scary/2025-06-25/output_0.json'
        # expected_output_file = 'tests/validation_output/scary/2025-06-25/output_0.json'
        expected_output_file = validated_data / 'scary/2025-06-25/output_0.json'
        validation_manager.run_validation()

        with open(output_file, 'r') as f:
            output = f.read()

        with open(expected_output_file, 'r') as f:
            expected_output = f.read()

        assert output == expected_output

