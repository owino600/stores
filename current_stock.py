#!/usr/bin/python3
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base
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
        """
        Updates the quantity and unit cost of the current stock.
        Args:
            quantity (int): The amount of stock to receive.
            unit_cost (float): The cost of each unit of stock.

        Returns:
            None
        """
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        if unit_cost <= 0:
            raise ValueError("Unit cost must be greater than 0")
        self.quantity += quantity
        self.unit_cost = unit_cost

    def issue_stock(self, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        if quantity > self.quantity:
            raise ValueError("Not enough stock available")
        self.quantity -= quantity

    def get_stock_level(self):
        """
        Get the stock level of the current stock.

        Returns:
            int: The quantity of the current stock.
        """
        return self.quantity

    def get_total_cost(self):
        """
        Calculate the total cost of the current stock.

        Returns:
            float: The total cost of the current stock.
        """
        return self.unit_cost * self.quantity

    def change_supplier(self, new_supplier):
        self.supplier = new_supplier

    def get_supplier_details(self):
        return self.supplier