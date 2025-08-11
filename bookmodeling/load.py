import os
from pathlib import Path
import json
from typing import Dict, Any, List, Set
import sqlalchemy
from sqlalchemy import create_engine, column, insert, bindparam
from sqlalchemy_utils import database_exists, create_database
from bookmodeling.db_models import Book, Base, book_table_clause, \
    author_table_clause, category_table_clause, identifier_table_clause, record_table_clause, book_author_clause, \
    book_category_clause
from bookmodeling.utils import get_latest_dir
from sqlalchemy import select
from logging import getLogger

logger = getLogger(__name__)

def _get_existing_books(conn: sqlalchemy.Connection, data_list: List[Dict[str, Any]]) -> Set[str]:
    all_books_set = {book['id'] for book in data_list}
    book_id = column('id')
    book_table = Book.__table__

    stmt = select(book_id).select_from(book_table).where(book_table.c.id.in_(all_books_set))
    existing_books = conn.execute(stmt).scalars()

    return set(existing_books)

def _get_book_dict(book_info: Dict[str, Any]):
    volume_info = book_info['volumeInfo']

    book_dict = {
        'id': book_info['id'],
        'title': volume_info['title'],
        'subtitle': volume_info['subtitle'],
        'publisher': volume_info['publisher'],
        'publishedDate': volume_info['publishedDate'],
        'pageCount': volume_info['pageCount'],
        'maturityRating': volume_info['maturityRating'],
        'language': volume_info['language']
    }

    return book_dict

def _get_identifiers(book_info: Dict[str, Any]):
    identifiers = book_info['volumeInfo']['industryIdentifiers']
    identifier_list = []

    if identifiers:
        for id_dict in identifiers:
            identifier_list.append({
                'id': id_dict['identifier'],
                'type': id_dict['type'],
                'bookID': book_info['id']
            })

    return identifier_list

def _load_books(conn: sqlalchemy.Connection, new_books: List[Dict[str, Any]]):

    insert_stmt = insert(book_table_clause).values(
        id=bindparam('id'),
        title=bindparam('title'),
        subtitle=bindparam('subtitle'),
        publisher=bindparam('publisher'),
        publishedDate=bindparam('publishedDate'),
        pageCount=bindparam('pageCount'),
        maturityRating=bindparam('maturityRating'),
        language=bindparam('language'),
    )
    conn.execute(insert_stmt, new_books)

def _load_authors(conn: sqlalchemy.Connection, author_set: Set[str]):

    select_stmt = select(author_table_clause.c.id).where(author_table_clause.c.name.in_(author_set))

    res = conn.execute(select_stmt).scalars()

    # set of authors already in database
    existing_authors = set(res.fetchall())
    new_authors = author_set - existing_authors

    insert_stmt = insert(author_table_clause).values(name=bindparam('name'))
    new_author_dicts = [{'name': author} for author in new_authors]

    conn.execute(insert_stmt, new_author_dicts)

def _load_categories(conn: sqlalchemy.Connection, category_set: Set[str]):

    select_stmt = select(category_table_clause.c.id).where(category_table_clause.c.name.in_(category_set))

    res = conn.execute(select_stmt).scalars()

    # set of categories already in database
    existing_categories = set(res.fetchall())
    new_categories = category_set - existing_categories

    insert_stmt = insert(category_table_clause).values(name=bindparam('name'))
    new_category_dicts = [{'name': category} for category in new_categories]

    conn.execute(insert_stmt, new_category_dicts)

def _load_identifiers(conn: sqlalchemy.Connection, identifier_list: List[Dict[str, str]]):
    insert_stmt = (insert(identifier_table_clause)
            .values(id=bindparam('id'), type=bindparam('type'), bookID=bindparam('bookID')))

    conn.execute(insert_stmt, identifier_list)

def _get_author_dict(conn: sqlalchemy.Connection, author_set: Set[str]):
    select_stmt = select(author_table_clause).where(author_table_clause.c.name.in_(author_set))
    result = conn.execute(select_stmt)
    author_sequence = result.fetchall()

    return {row.name: row.id for row in author_sequence}

def _get_category_dict(conn: sqlalchemy.Connection, category_set: Set[str]):
    select_stmt = select(category_table_clause).where(category_table_clause.c.name.in_(category_set))
    result = conn.execute(select_stmt)
    category_sequence = result.fetchall()

    return {row.name: row.id for row in category_sequence}

def _get_book_authors(book_info: Dict[str, Any], author_dict: Dict[str, int]):
    book_id = book_info['id']
    authors = book_info['volumeInfo']['authors']

    if authors:
        return [{'bookID': book_id, 'authorID': author_dict[author]} for author in authors]

    return []

def _get_book_categories(book_info: Dict[str, Any], category_dict: Dict[str, int]):
    book_id = book_info['id']
    categories = book_info['volumeInfo']['categories']

    if categories:
        return [{'bookID': book_id, 'categoryID': category_dict[category]} for category in categories]

    return []

def _get_record_dict(book_info: Dict[str, Any], record_date: str):
    volume_info = book_info['volumeInfo']
    sale_info = book_info['saleInfo']
    access_info = book_info['accessInfo']

    record_dict = {
        'averageRating': volume_info['averageRating'],
        'ratingsCount': volume_info['ratingsCount'],
        'saleCountry': None,
        'saleability': None,
        'isEbook': None,
        'listPrice': None,
        'retailPrice': None,
        'accessCountry': None,
        'viewability': None,
        'textToSpeech': None,
        'EPubAvailable': None,
        'PDFAvailable': None,
        'recordDate': record_date,
        'bookID': book_info['id']
    }

    if sale_info:
        record_dict['saleCountry'] = sale_info['country']
        record_dict['saleability'] = sale_info['saleability']
        record_dict['isEbook'] = sale_info['isEbook']

        if sale_info['listPrice']:
            record_dict['listPrice'] = sale_info['listPrice']['amount']
        if sale_info['retailPrice']:
            record_dict['retailPrice'] = sale_info['retailPrice']['amount']

    if access_info:
        epub = access_info['epub']
        pdf = access_info['pdf']

        record_dict['accessCountry'] = access_info['country']
        record_dict['viewability'] = access_info['viewability']
        record_dict['textToSpeech'] = access_info['textToSpeechPermission']

        if epub:
            record_dict['EPubAvailable'] = epub['isAvailable']
        if pdf:
            record_dict['PDFAvailable'] = pdf['isAvailable']

    return record_dict

def _load_book_records(conn: sqlalchemy.Connection, book_records: List[Dict[str, Any]]) -> None:
    insert_stmt = insert(record_table_clause).values(
        averageRating=bindparam('averageRating'),
        ratingsCount=bindparam('ratingsCount'),
        saleCountry=bindparam('saleCountry'),
        saleability=bindparam('saleability'),
        isEbook=bindparam('isEbook'),
        listPrice=bindparam('listPrice'),
        retailPrice=bindparam('retailPrice'),
        accessCountry=bindparam('accessCountry'),
        viewability=bindparam('viewability'),
        textToSpeech=bindparam('textToSpeech'),
        EPubAvailable=bindparam('EPubAvailable'),
        PDFAvailable=bindparam('PDFAvailable'),
        recordDate=bindparam('recordDate'),
        bookID=bindparam('bookID')
    )

    conn.execute(insert_stmt, book_records)

def _load_book_authors(conn: sqlalchemy.Connection, book_author_list: List[Dict[str, Any]]):
    insert_stmt = insert(book_author_clause).values(bookID=bindparam('bookID'), authorID=bindparam('authorID'))

    conn.execute(insert_stmt, book_author_list)

def _load_book_categories(conn: sqlalchemy.Connection, book_category_list: List[Dict[str, Any]]):
    insert_stmt = insert(book_category_clause).values(bookID=bindparam('bookID'), categoryID=bindparam('categoryID'))

    conn.execute(insert_stmt, book_category_list)

def _process_data(conn: sqlalchemy.Connection, data_list: List[Dict[str, Any]], record_date: str) -> None:
    # If book is in table
        # Add book record for it
    # If book is not in table:
        # Add book to table
        # Add authors to table
        # Add book authors to table
        # Add categories to table
        # Add book categories to table
        # Add industry identifiers to table
        # Add book record for it

    new_books = []
    new_book_ids = set()
    author_set = set()
    category_set = set()
    industry_identifiers = []
    book_author_list = []
    book_category_list = []
    book_records = []

    existing_books = _get_existing_books(conn, data_list)
    for book_info in data_list:
        if book_info['id'] not in existing_books and book_info['id'] not in new_book_ids:
            authors = book_info['volumeInfo']['authors']
            categories = book_info['volumeInfo']['categories']

            new_books.append(_get_book_dict(book_info))
            if authors:
                author_set.update(authors)
            if categories:
                category_set.update(categories)
            industry_identifiers.extend(_get_identifiers(book_info))

            # Handle duplicate books.
            new_book_ids.add(book_info['id'])

    if new_books:
        _load_books(conn, new_books)
    if author_set:
        _load_authors(conn, author_set)
    if category_set:
        _load_categories(conn, category_set)
    if industry_identifiers:
        _load_identifiers(conn, industry_identifiers)

    author_dict = _get_author_dict(conn, author_set)
    category_dict = _get_category_dict(conn, category_set)

    for book_info in data_list:
        if book_info['id'] in new_book_ids:
            book_author_list.extend(_get_book_authors(book_info, author_dict))
            book_category_list.extend(_get_book_categories(book_info, category_dict))
            new_book_ids.remove(book_info['id'])

        book_records.append(_get_record_dict(book_info, record_date))

    _load_book_records(conn, book_records)
    if book_author_list:
        _load_book_authors(conn, book_author_list)
    if book_category_list:
        _load_book_categories(conn, book_category_list)

    conn.commit()


def _process_files(conn: sqlalchemy.Connection, latest_keyword_dir: Path) -> None:
    data_list = []
    record_date = str(latest_keyword_dir.name)

    # Gather data from all files in latest keyword directory.
    for file in latest_keyword_dir.iterdir():
        with open(file, 'r') as f:
            data_list.extend(json.loads(f.read()))

    _process_data(conn, data_list, record_date)




def _create_tables(engine: sqlalchemy.engine.Engine) -> None:
    # Create database if necessary
    if not database_exists(engine.url):
        create_database(engine.url)

    # Create tables if necessary
    Base.metadata.create_all(engine)


def load_data(keywords: list[str], input_path: str, date: str|None = None):
    """ Load data from input path into database for keywords specified.

    Args:
        keywords: A list of keywords specifying which data should be loaded into the database.
        input_path: The input directory containing the validated data.
        date: An optional parameter specifying a date if older data should be loaded.

    Returns:
        None
    """

    engine = create_engine(os.environ.get('DB_URL'))
    _create_tables(engine)

    with engine.connect() as conn:
        for keyword in keywords:
            logger.info(f'Processing keyword: {keyword}')
            keyword_dir = Path(input_path) / keyword
            if not date:
                latest_date = get_latest_dir(keyword_dir)
            else:
                latest_date = date
            latest_keyword_dir = keyword_dir / latest_date
            if latest_keyword_dir.exists():
                logger.info(f'Processing date: {latest_date}')
                _process_files(conn, latest_keyword_dir)
            else:
                logger.warning(f'{keyword}/{latest_date} directory does not exist')


