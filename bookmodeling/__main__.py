import logging
from .api_request import search_google_keywords

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

    search_google_keywords(keywords, 2, 10)


main()
