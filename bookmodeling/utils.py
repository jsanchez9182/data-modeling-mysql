from pathlib import Path
from datetime import date
import datetime
import logging

logger = logging.getLogger()

from bookmodeling.exceptions import MissingDirectoriesException


def get_latest_dir(input_keyword_dir: Path) -> Path:
    """

    Args:
        input_keyword_dir: Path to the keyword directory in the input directory.

    Returns:
        Path to the latest date directory in the keyword directory.
    """
    date_fmt = '%Y-%m-%d'
    latest_date = date(datetime.MINYEAR, 1, 1)

    for item in input_keyword_dir.iterdir():
        dir_date = datetime.datetime.strptime(item.name, date_fmt).date()
        latest_date = max(latest_date, dir_date)

    # If no folders in the keyword folder
    if latest_date == date(datetime.MINYEAR, 1, 1):
        keyword_dir = input_keyword_dir.name
        logger.error(f'No directories in {keyword_dir} directory.')
        raise MissingDirectoriesException(keyword_dir)

    return Path(latest_date.strftime(date_fmt))