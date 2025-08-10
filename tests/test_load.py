import copy
import datetime
from decimal import Decimal
import sqlalchemy
from sqlalchemy import select, TableClause, join
from bookmodeling.load import load_data
from bookmodeling.db_models import Base, author_table_clause, book_table_clause, category_table_clause, \
    identifier_table_clause, record_table_clause, book_category_clause, book_author_clause


class ExpectedSnapshot:
    def __init__(self, books, authors, categories, identifiers, book_records, book_authors, book_categories):
        self.books = books
        self.authors = authors
        self.categories = categories
        self.identifiers = identifiers
        self.book_records = book_records
        self.book_authors = book_authors
        self.book_categories = book_categories


expected1_books = [
    ('4OfeCgAAQBAJ', '1001 Ways to Be Romantic', None, 'Sourcebooks, Inc.',
     datetime.date(2010, 1, 1), 456, 'NOT_MATURE', 'en'),
    ('Af_aMKNJ2oEC', 'The Complete Guide to Everything Romantic', 'A Book for Lovers',
     'Carol Publishing Corporation', datetime.date(1995, 1, 1),
     248, 'MATURE', 'en')
]

expected1_authors = [
    ('Michael Newman',)
]

expected1_categories = [
    ('Family & Relationships',)
]
expected1_identifiers = [
    ('0806515473', 'ISBN_10', 'Af_aMKNJ2oEC'),
    ('1402244096', 'ISBN_10', '4OfeCgAAQBAJ'),
    ('9780806515472', 'ISBN_13', 'Af_aMKNJ2oEC'),
    ('9781402244094', 'ISBN_13', '4OfeCgAAQBAJ'),
]

expected1_book_records = [
    (1, None, None, 'US', 'NOT_FOR_SALE', 0, None, None, 'US', 'NO_PAGES', 'ALLOWED', 0, 0,
     datetime.date(2025, 8, 5), 'Af_aMKNJ2oEC'),
    (2, None, None, 'US', 'NOT_FOR_SALE', 0, None, None, 'US', 'PARTIAL', 'ALLOWED', 0, 1,
     datetime.date(2025, 8, 5), '4OfeCgAAQBAJ'),
]

expected1_book_categories = [
    ('4OfeCgAAQBAJ', 'Family & Relationships'),
    ('Af_aMKNJ2oEC', 'Family & Relationships')
]

expected1_book_authors = [
    ('4OfeCgAAQBAJ', 'Michael Newman'),
    ('Af_aMKNJ2oEC', 'Michael Newman')
]

expected1 = ExpectedSnapshot(expected1_books, expected1_authors, expected1_categories, expected1_identifiers,
                             expected1_book_records, expected1_book_authors, expected1_book_categories)

expected2 = copy.deepcopy(expected1)

expected2.book_records.extend([
    (3, None, None, 'US', 'NOT_FOR_SALE', 0, None, None, 'US', 'NO_PAGES', 'ALLOWED', 0, 0,
     datetime.date(2025, 8, 7), 'Af_aMKNJ2oEC'),
    (4, 3.7, 10, 'US', 'FOR_SALE', 0, Decimal('5.00'), Decimal('5.00'), 'US', 'PARTIAL', 'ALLOWED', 1, 1,
     datetime.date(2025, 8, 7), '4OfeCgAAQBAJ')
])

expected3_books = [
    ('4OfeCgAAQBAJ', '1001 Ways to Be Romantic', None, 'Sourcebooks, Inc.', datetime.date(2010, 1, 1), 456,
     'NOT_MATURE', 'en'),
    ('Af_aMKNJ2oEC', 'The Complete Guide to Everything Romantic', 'A Book for Lovers', 'Carol Publishing Corporation',
     datetime.date(1995, 1, 1), 248, 'MATURE', 'en'),
    ('WkuREAAAQBAJ', 'The Scary Book', None, 'National Geographic Books', datetime.date(2020, 1, 1), 0,
     'NOT_MATURE', 'en'),
    ('Zs7rAwAAQBAJ', 'Not Very Scary', None, 'Farrar, Straus and Giroux (BYR)',
     datetime.date(2014, 8, 12), 40, 'NOT_MATURE', 'en')
]
expected3_authors = [
    ('Carol Brendler',),
    ('Michael Newman',),
    ('Thierry Dedieu',),
]
expected3_categories = [
    ('Family & Relationships',),
    ('Juvenile Fiction',)
]
expected3_identifiers = [
    ('0806515473', 'ISBN_10', 'Af_aMKNJ2oEC'),
    ('1402244096', 'ISBN_10', '4OfeCgAAQBAJ'),
    ('1466875372', 'ISBN_10', 'Zs7rAwAAQBAJ'),
    ('3791374648', 'ISBN_10', 'WkuREAAAQBAJ'),
    ('9780806515472', 'ISBN_13', 'Af_aMKNJ2oEC'),
    ('9781402244094', 'ISBN_13', '4OfeCgAAQBAJ'),
    ('9781466875371', 'ISBN_13', 'Zs7rAwAAQBAJ'),
    ('9783791374642', 'ISBN_13', 'WkuREAAAQBAJ'),
]
expected3_book_records = [
    (1, None, None, 'US', 'NOT_FOR_SALE', 0, None, None, 'US', 'NO_PAGES', 'ALLOWED', 0, 0,
     datetime.date(2025, 8, 7), 'Af_aMKNJ2oEC'),
    (2, 3.7, 10, 'US', 'FOR_SALE', 0, Decimal('5.00'), Decimal('5.00'), 'US', 'PARTIAL', 'ALLOWED',
     1, 1, datetime.date(2025, 8, 7), '4OfeCgAAQBAJ'),
    (3, None, None, 'US', 'NOT_FOR_SALE', 0, None, None, 'US', 'NO_PAGES', 'ALLOWED', 0, 0,
     datetime.date(2025, 6, 25), 'WkuREAAAQBAJ'),
    (4, None, None, 'US', 'FOR_SALE', 1, Decimal('14.99'), Decimal('14.99'), 'US', 'PARTIAL', 'ALLOWED', 1, 1,
     datetime.date(2025, 6, 25), 'Zs7rAwAAQBAJ')
]

expected3_book_categories = [
    ('4OfeCgAAQBAJ', 'Family & Relationships'),
    ('Af_aMKNJ2oEC', 'Family & Relationships'),
    ('WkuREAAAQBAJ', 'Juvenile Fiction'),
    ('Zs7rAwAAQBAJ', 'Juvenile Fiction')
]

expected3_book_authors = [
    ('4OfeCgAAQBAJ', 'Michael Newman'),
    ('Af_aMKNJ2oEC', 'Michael Newman'),
    ('WkuREAAAQBAJ', 'Thierry Dedieu'),
    ('Zs7rAwAAQBAJ', 'Carol Brendler')
]

expected3 = ExpectedSnapshot(expected3_books, expected3_authors, expected3_categories, expected3_identifiers,
                             expected3_book_records, expected3_book_authors, expected3_book_categories)


class DBSnapshot:
    def __init__(self, conn: sqlalchemy.Connection):
        self.conn = conn
        self.books = self.get_all_results(book_table_clause)
        self.authors = self.get_all_names(author_table_clause)
        self.categories = self.get_all_names(category_table_clause)
        self.identifiers = self.get_all_results(identifier_table_clause)
        self.book_records = self.get_all_results(record_table_clause)
        self.book_categories = self.get_book_categories()
        self.book_authors = self.get_book_authors()

    def get_all_results(self, table_clause: TableClause):
        order_col = table_clause.c.id if 'id' in table_clause.columns else table_clause.c.bookID
        select_stmt = select(table_clause).order_by(order_col)
        res = self.conn.execute(select_stmt)

        return res.fetchall()

    def get_all_names(self, table_clause: TableClause):
        order_col = table_clause.c.name
        select_stmt = select(table_clause.c.name).select_from(table_clause).order_by(order_col)
        res = self.conn.execute(select_stmt)

        return res.fetchall()

    def get_book_authors(self):
        order_col = book_author_clause.c.bookID
        j = join(book_author_clause, author_table_clause,
                 book_author_clause.c.authorID == author_table_clause.c.id)

        select_stmt = (select(book_author_clause.c.bookID, author_table_clause.c.name).select_from(j)
                       .order_by(order_col))

        res = self.conn.execute(select_stmt)
        return res.fetchall()

    def get_book_categories(self):
        order_col = book_category_clause.c.bookID
        j = join(book_category_clause, category_table_clause,
                 book_category_clause.c.categoryID == category_table_clause.c.id)

        select_stmt = (select(book_category_clause.c.bookID, category_table_clause.c.name).select_from(j)
                       .order_by(order_col))

        res = self.conn.execute(select_stmt)
        return res.fetchall()


class TestLoadData:
    def test_old_dir(self, validated_data, conn):
        # Test that the load operation words on older directories.
        load_data(['romantic'], str(validated_data), '2025-08-05')
        actual = DBSnapshot(conn)

        assert actual.books == expected1.books
        assert actual.authors == expected1.authors
        assert actual.categories == expected1.categories
        assert actual.identifiers == expected1.identifiers
        assert actual.book_records == expected1.book_records
        assert actual.book_authors == expected1.book_authors
        assert actual.book_categories == expected1.book_categories

    def test_multiple_dates_same_keyword(self, validated_data, conn):
        # Test that multiple data loads don't cause errors.
        load_data(['romantic'], str(validated_data), '2025-08-05')
        load_data(['romantic'], str(validated_data))
        actual = DBSnapshot(conn)

        assert actual.books == expected2.books
        assert actual.authors == expected2.authors
        assert actual.categories == expected2.categories
        assert actual.identifiers == expected2.identifiers
        assert actual.book_records == expected2.book_records
        assert actual.book_authors == expected2.book_authors
        assert actual.book_categories == expected2.book_categories

    def test_multiple_keywords(self, validated_data, conn):
        # Test that data from different directories is added to db during load.
        load_data(['romantic','scary'], str(validated_data))
        actual = DBSnapshot(conn)

        assert actual.books == expected3.books
        assert actual.authors == expected3.authors
        assert actual.categories == expected3.categories
        assert actual.identifiers == expected3.identifiers
        assert actual.book_records == expected3.book_records
        assert actual.book_authors == expected3.book_authors
        assert actual.book_categories == expected3.book_categories

    def test_nonexistent_directory(self, validated_data, conn, caplog):
        # There should be no data if the directory is empty and a message should be logged.
        load_data(['romantic'], str(validated_data), '2025-07-03')
        actual = DBSnapshot(conn)

        assert actual.books == []
        assert actual.authors == []
        assert actual.categories == []
        assert actual.identifiers == []
        assert actual.book_records == []
        assert actual.book_authors == []
        assert actual.book_categories == []
        assert caplog.records[0].msg == "romantic/2025-07-03 directory does not exist"