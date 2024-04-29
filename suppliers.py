#!/usr/bin/python3
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Supplier(Base):
    __tablename__ = 'supplier'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    contact_info = Column(String)
    email = Column(String)
    stocks = relationship('STOCK', back_populates='supplier')