from sqlalchemy import String, Table, Column, ForeignKey, table, column
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy.types import DECIMAL
from typing import Optional, List
import datetime
import decimal


class Base(DeclarativeBase):
    pass


class Author(Base):
    __tablename__ = 'author'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(60))

author_table_clause = table(
    Author.__tablename__,
    column('id'),
    column('name')
)


book_author = Table(
    'book_author',
    Base.metadata,
    Column('bookID', ForeignKey('book.id'), primary_key=True),
    Column('authorID', ForeignKey('author.id'), primary_key=True)
)

book_author_clause = table(
    book_author.name,
    *[column(col.name) for col in book_author.columns]
)


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(60))

category_table_clause = table(
    Category.__tablename__,
    column('id'),
    column('name')
)

book_category = Table(
    'book_category',
    Base.metadata,
    Column('bookID', ForeignKey('book.id'), primary_key=True),
    Column('categoryID', ForeignKey('category.id'), primary_key=True)
)

book_category_clause = table(
    book_category.name,
    *[column(col.name) for col in book_category.columns]
)


class BookRecord(Base):
    __tablename__ = 'book_record'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    averageRating: Mapped[Optional[float]]
    ratingsCount: Mapped[Optional[int]]
    saleCountry: Mapped[Optional[str]] = mapped_column(String(5))
    saleability: Mapped[Optional[str]] = mapped_column(String(20))
    isEbook: Mapped[Optional[bool]]
    listPrice: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(8, 2))
    retailPrice: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(8, 2))
    accessCountry: Mapped[Optional[str]] = mapped_column(String(5))
    viewability: Mapped[Optional[str]] = mapped_column(String(20))
    textToSpeech: Mapped[Optional[str]] = mapped_column(String(30))
    EPubAvailable: Mapped[Optional[bool]]
    PDFAvailable: Mapped[Optional[bool]]
    recordDate: Mapped[datetime.date]
    bookID: Mapped[str] = mapped_column(ForeignKey("book.id"))

record_table_clause = table(
    BookRecord.__tablename__,
    column('id'),
    column('averageRating'),
    column('ratingsCount'),
    column('saleCountry'),
    column('saleability'),
    column('isEbook'),
    column('listPrice'),
    column('retailPrice'),
    column('accessCountry'),
    column('viewability'),
    column('textToSpeech'),
    column('EPubAvailable'),
    column('PDFAvailable'),
    column('recordDate'),
    column('bookID')
)

class IndustryIdentifier(Base):
    __tablename__ = 'industry_identifier'
    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    type: Mapped[str] = mapped_column(String(8))
    bookID: Mapped[str] = mapped_column(ForeignKey("book.id"))

identifier_table_clause = table(
    IndustryIdentifier.__tablename__,
    column('id'),
    column('type'),
    column('bookID'),
)


class Book(Base):
    __tablename__ = 'book'

    id: Mapped[str] = mapped_column(String(16), primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    subtitle: Mapped[Optional[str]] = mapped_column(String(200))
    publisher: Mapped[Optional[str]] = mapped_column(String(100))
    publishedDate: Mapped[Optional[datetime.date]]
    pageCount: Mapped[Optional[int]]
    maturityRating: Mapped[Optional[str]] = mapped_column(String(30))
    language: Mapped[Optional[str]] = mapped_column(String(5))
    authors: Mapped[List[Author]] = relationship(secondary=book_author)
    categories: Mapped[List[Category]] = relationship(secondary=book_category)
    bookRecords: Mapped[List[BookRecord]] = relationship()
    industryIdentifiers: Mapped[List[IndustryIdentifier]] = relationship()


book_table_clause = table(
    Book.__tablename__,
    column('id'),
    column('title'),
    column('subtitle'),
    column('publisher'),
    column('publishedDate'),
    column('pageCount'),
    column('maturityRating'),
    column('language')
)
