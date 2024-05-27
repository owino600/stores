#!/usr/bin/python3

from current_stock import Supplier, STOCK
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base

classes = {"current_stock":STOCK, "suppliers":Supplier}

class DB_STORAGE:
    """interact with the MYSQL database"""
    __engine = None
    __session = None
    
    def __init__(self):
        """insantiate a DB Storage"""
        
        STORE_MYSQL_USER = getenv('STORE_MYSQL_USER')
        STORE_MYSQL_PWD = getenv('STORE_MYSQL_PWD')
        STORE_MYSQL_HOST = getenv('STORE_MYSQL_HOST')
        STORE_MYSQL_DB = getenv('STORE_MYSQL_DB')
        self.__engine = create_engine("mysql+mysqlconnector://{}:{}@{}/{}".format(
          STORE_MYSQL_USER,
          STORE_MYSQL_PWD,
          STORE_MYSQL_HOST,
          STORE_MYSQL_DB  
        ))
        
    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()
    def get(self, cls, id):
        """Retrieve one object"""
        if cls not in classes:
            return None
        return self.__session.query(classes[cls]).get(id)