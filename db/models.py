from . import *
from db.database import Base
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String, Float, DateTime, Enum, Boolean
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from schemas.bid import BidStatus
from schemas.product import ConditionEnum


class DbUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    address = relationship("DbAddress", back_populates="user",  cascade="all, delete-orphan")
    products_selling = relationship("DbProduct", back_populates="seller", cascade="all, delete-orphan",
                                    foreign_keys="[DbProduct.seller_id]")
    products_buying = relationship("DbProduct", back_populates="buyer",
                                   foreign_keys="[DbProduct.buyer_id]")
    bids = relationship("DbBid", back_populates="user", cascade="all, delete-orphan")
    # Define relationship to DbPayment
    payments = relationship("DbPayment", back_populates="user", cascade="all, delete-orphan")


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
    seller = relationship("DbUser", back_populates="products_selling", foreign_keys="[DbProduct.seller_id]")
    buyer = relationship("DbUser", back_populates="products_buying", foreign_keys="[DbProduct.buyer_id]")
    bids = relationship("DbBid", back_populates="product", cascade="all, delete-orphan")
    payment_id = Column(Integer, ForeignKey("payments.id"))
    payment = relationship("DbPayment", back_populates="items")


class DbBid(Base):
    __tablename__ = 'bids'
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime)
    status = Column(Enum(BidStatus))
    product_id = Column(Integer, ForeignKey('products.id'))
    price = Column(Float)
    bidder_id = Column(Integer, ForeignKey('users.id'))
    product = relationship("DbProduct", back_populates="bids")
    user = relationship("DbUser", back_populates="bids")


class DbPayment(Base):
    __tablename__ = 'payments'
    id = Column(String, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Float)
    status = Column(String)
    description = Column(String)
    user = relationship('DbUser', back_populates='payments')
    items = relationship("DbProduct", back_populates="payment")
