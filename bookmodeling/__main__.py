import logging
from .api_request import search_google_keywords
from .load import load_data
from .validators import validate_keywords

formatter = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - Line %(lineno)d - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def main():

    keywords = [
        'adventure',
        'exciting',
        'haunted',
        'historic',
        'romantic',
        'scary',
        'thrilling'
    ]

    search_google_keywords(keywords, 1, 40, 'raw_data')
    validate_keywords(keywords, 'raw_data', 'validated_data', 70)
    load_data(keywords, 'validated_data')
