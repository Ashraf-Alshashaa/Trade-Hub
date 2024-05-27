from . import *
from db.database import Base
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String, Float, DateTime, Enum, Boolean
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from schemas.bid import BidStatus
from schemas.product import StateEnum, ConditionEnum


class DbUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    address = relationship("DbAddress", back_populates="user")


class DbAddress(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True, index=True)
    street_name = Column(String)
    city = Column(String)
    country = Column(String)
    postcode = Column(String)
    house_number = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    default = Column(Boolean, nullable=False)
    user = relationship("DbUser", back_populates="address")


class DbProduct(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    image = Column(String)
    description = Column(String)
    seller_id = Column(Integer, ForeignKey('users.id'))
    buyer_id = Column(Integer, ForeignKey('users.id'))
    price = Column(Float)
    date = Column(DateTime)
    condition = Column(Enum(ConditionEnum))
    state = Column(Enum(StateEnum))



class DbBid(Base):
    __tablename__ = 'bids'
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime)
    status = Column(Enum(BidStatus))
    product_id = Column(Integer, ForeignKey('products.id'))
    price = Column(Float)
    bidder_id = Column(Integer, ForeignKey('users.id'))
