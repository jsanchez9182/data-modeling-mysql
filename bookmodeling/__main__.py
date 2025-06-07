import logging
from .api_request import BookRequest

formatter = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - Line %(lineno)d - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def main():
    book_request = BookRequest('flowers', 5,7, 20)
    book_request.get_data()

main()
