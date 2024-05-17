from db.database import Base
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String, Float, Enum, DateTime
from datetime import datetime
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship


class DbUser(Base):
    __tablename__='users'
    id = Column(Integer, primary_key=True, index=True)
    username=Column(String)
    email=Column(String)
    password=Column(String)
    address_id = Column(Integer)

class DbAddress(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True, index=True)
    street_name = Column(String)
    city = Column(String)
    country = Column(String)
    postcode = Column(String)
    house_number = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))

class DbProduct(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    image=Column(String)
    description = Column(String)
    seller_id = Column(Integer, ForeignKey('users.id'))
    buyer_id = Column(Integer, ForeignKey('users.id'))
    price = Column(Float)
    # datetime requires a certain configuration which stops testing the other properties, therefore for now I changed it to str
    date = Column(String)
    condition = Column(Enum)
    state = Column(Enum)

class DbBid(Base):
    __tablename__ = 'bids'
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    price=Column(Float)
    bidder_id = Column(Integer, ForeignKey('users.id'))