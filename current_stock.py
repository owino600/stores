#!/usr/bin/python3
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class STOCK(Base):
    __tablename__ = 'current_stock'

    id = Column(Integer, primary_key=True)
    item_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    supplier = Column(String, nullable=False)
    unit_cost = Column(Float)
    supplier_id = Column(Integer, ForeignKey('supplier.id'))
    supplier = relationship('Supplier', back_populates='stocks')


    def __init__(self, item_name, quantity, supplier, unit_cost):
        self.item_name = item_name
        self.quantity = quantity
        self.supplier = supplier
        self.unit_cost = unit_cost

    def receive_stock(self, quantity, unit_cost):
        self.quantity += quantity
        self.unit_cost = unit_cost

    def issue_stock(self, quantity):
        if quantity > self.quantity:
            print("Not enough stock available")
            return
        self.quantity -= quantity

    def get_stock_level(self):
        return self.quantity

    def get_total_cost(self):
        return self.unit_cost * self.quantity

    def change_supplier(self, new_supplier):
        self.supplier = new_supplier

    def get_supplier_details(self):
        return self.supplier