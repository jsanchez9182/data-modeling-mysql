from pathlib import Path

from pydantic import BaseModel, BeforeValidator, ValidationError, Field
from typing import Optional, List, Annotated
from datetime import date
from decimal import Decimal
import json
import logging
from bookmodeling.exceptions import MissingDataException, ValidationPercentException, MissingDirectoriesException, \
    MissingFilesException
from bookmodeling.utils import get_latest_dir

logger = logging.getLogger(__name__)


def add_day(val):
    if type(val) == str:
        if len(val) == 4:
            val += '-01'
        if len(val) == 7:
            val += '-01'

    return val


# If date is missing -mm and/or -dd portion of yyyy-mm-dd they are initialized to 01.
InitializedDate = Annotated[date, BeforeValidator(add_day)]


class IndustryIdentifier(BaseModel):
    type: str = Field(max_length=8, default=None)
    identifier: str = Field(max_length=40, default=None)


class ListPrice(BaseModel):
    amount: Decimal


class RetailPrice(BaseModel):
    amount: Decimal


class SaleInfo(BaseModel):
    country: str = Field(max_length=5, default=None)
    saleability: str = Field(max_length=20, default=None)
    isEbook: bool
    listPrice: Optional[ListPrice] = None
    retailPrice: Optional[RetailPrice] = None


class EPub(BaseModel):
    isAvailable: bool


class PDF(BaseModel):
    isAvailable: bool


class AccessInfo(BaseModel):
    country: str = Field(max_length=5, default=None)
    viewability: str = Field(max_length=20, default=None)
    textToSpeechPermission: str = Field(max_length=30, default=None)
    epub: Optional[EPub] = None
    pdf: Optional[PDF] = None


MAX_AUTHOR_LEN = Annotated[str, Field(max_length=60)]
MAX_CATEGORY_LEN = Annotated[str, Field(max_length=60)]

class VolumeInfo(BaseModel):
    title: str = Field(max_length=200)
    subtitle: Optional[str] = Field(max_length=200, default=None)
    authors: Optional[List[MAX_AUTHOR_LEN]] = None
    publisher: Optional[str] = Field(max_length=100, default=None)
    publishedDate: Optional[InitializedDate] = None
    industryIdentifiers: Optional[List[IndustryIdentifier]] = None
    pageCount: Optional[int] = None
    categories: Optional[List[MAX_CATEGORY_LEN]] = None
    averageRating: Optional[float] = None
    ratingsCount: Optional[int] = None
    maturityRating: Optional[str] = Field(max_length=30, default=None)
    language: Optional[str] = Field(max_length=5, default=None)


class Volume(BaseModel):
    id: str
    volumeInfo: VolumeInfo
    saleInfo: Optional[SaleInfo] = None
    accessInfo: Optional[AccessInfo] = None


def _write_data(latest_output_dir: Path, validated_records: List[str]) -> None:
    # write list of json strings into output_0.json in latest_output_dir
    latest_output_dir.mkdir(parents=True)
    output_file = latest_output_dir / 'output_0.json'

    with open(output_file, 'w') as f:
        # Load each json encoded string into list and dump list to avoid double encoding.
        json.dump([json.loads(i) for i in validated_records], f, indent=2)


class ValidationManager:
    def __init__(self, input_dir: str, output_dir: str, keyword: str, min_percent: int = 70):
        self._keyword_input_dir = input_dir + '/' + keyword
        self._keyword_output_dir = output_dir + '/' + keyword
        self._keyword = keyword
        self._sanitized_records = 0
        self._total_records = 0
        self._min_percent = min_percent

    def _validate_file(self, data_file: Path) -> List[str]:
        # Return a list of records from data_file that pass validation (in json string format).
        file_records = []
        with open(data_file, 'r') as f:
            content = json.load(f)

        for raw_record in content.get('items', []):
            try:
                record = Volume.model_validate(raw_record)
                self._sanitized_records += 1
                # Records are json encoded strings.
                file_records.append(record.model_dump_json())
            except ValidationError as e:
                for error in e.errors():
                    logger.warning(f'Msg: {error["msg"]}, Loc: {error["loc"]}')

            self._total_records += 1

        return file_records

    def _validate_directory(self, latest_input_dir: Path) -> List[str]:
        # Return a list of records from latest_input_dir that pass validation (in json string format).
        dir_records = []
        files = list(latest_input_dir.iterdir())

        # If no files in the latest directory
        if len(files) == 0:
            keyword_date_dir = latest_input_dir.parent.name + '/' + latest_input_dir.name
            logger.error(f'No files in the {keyword_date_dir} directory.')
            raise MissingFilesException(keyword_date_dir)

        for data_file in files:
            file_records = self._validate_file(data_file)
            dir_records.extend(file_records)

        if self._total_records == 0:
            logger.error("No records in the directory.")
            raise MissingDataException()

        percent_sanitized = (self._sanitized_records / self._total_records) * 100

        if percent_sanitized < self._min_percent:
            msg = (f"Excepted {float(self._min_percent)} percent of records"
                   f" to pass validation but only {percent_sanitized} passed.")
            logger.error(msg)
            raise ValidationPercentException(msg)

        return dir_records

    def run_validation(self) -> None:
        """
        Validate keyword data in the input_dir and output valid records to the output_dir.

        Returns: None
        """
        latest_date = get_latest_dir(Path(self._keyword_input_dir))
        latest_input_dir = self._keyword_input_dir / latest_date
        latest_output_dir = self._keyword_output_dir / latest_date

        validated_records = self._validate_directory(latest_input_dir)
        _write_data(latest_output_dir, validated_records)


def validate_keywords(keywords: list[str], input_dir: str, output_dir: str, min_percent: int) -> None:
    """
    Generates GoogleBooksClient and pulls data for each keyword.

    Args:
        keywords: List of keywords files to validated.
        input_dir: The directory where the raw data is stored.
        output_dir: The directory where the validated records will be stored.
        min_percent: Minimum percentage of passing records for a validation to be considered successful.

    Returns: None

    """
    for keyword in keywords:
        vm = ValidationManager(input_dir, output_dir, keyword, min_percent)
        vm.run_validation()
