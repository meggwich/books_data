from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    id_publisher = Column(Integer, ForeignKey('publisher.id'))

    publisher = relationship('Publisher', back_populates='books')

Publisher.books = relationship('Book', order_by=Book.id, back_populates='publisher')

class Shop(Base):
    __tablename__ = 'shop'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Stock(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey('book.id'))
    id_shop = Column(Integer, ForeignKey('shop.id'))
    count = Column(Integer)

    book = relationship('Book', back_populates='stocks')
    shop = relationship('Shop', back_populates='stocks')

Book.stocks = relationship('Stock', order_by=Stock.id, back_populates='book')
Shop.stocks = relationship('Stock', order_by=Stock.id, back_populates='shop')

class Sale(Base):
    __tablename__ = 'sale'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    date_sale = Column(Date)
    id_stock = Column(Integer, ForeignKey('stock.id'))
    count = Column(Integer)

    stock = relationship('Stock', back_populates='sales')

Stock.sales = relationship('Sale', order_by=Sale.id, back_populates='stock')






from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

# Создание сессии
engine = create_engine('postgresql://user:password@localhost/dbname')
Session = sessionmaker(bind=engine)
session = Session()

# Ввод имени или идентификатора издателя
publisher_name = input("Введите имя или идентификатор издателя: ")

# Запрос
query = select(Book.title, Shop.name, Sale.price, Sale.date_sale).\
    join(Stock, Book.id == Stock.id_book).\
    join(Sale, Stock.id == Sale.id_stock).\
    join(Shop, Stock.id_shop == Shop.id).\
    join(Publisher, Book.id_publisher == Publisher.id).\
    where(Publisher.name == publisher_name)

# Выполнение запроса и вывод результатов
for book_title, shop_name, sale_price, sale_date in session.execute(query):
    print(f"{book_title} | {shop_name} | {sale_price} | {sale_date}")


import json
import os

# Параметры подключения к БД
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')

# Создание сессии
engine = create_engine(f'postgresql://user:password@localhost/dbname')
Session = sessionmaker(bind=engine)
session = Session()

# Загрузка тестовых данных
with open('fixtures.json', 'r') as fd:
    data = json.load(fd)

# Заполнение БД
for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()