#!/usr/bin/python3
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.orm import relationship

Base = declarative_base()

class Supplier(Base):
    __tablename__ = 'supplier'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    stocks = relationship('STOCK', back_populates='supplier')

class STOCK(Base):
    __tablename__ = 'current_stock'

    id = Column(Integer, primary_key=True)
    item_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_cost = Column(Float)
    supplier_id = Column(Integer, ForeignKey('supplier.id'))
    supplier = relationship('Supplier', back_populates='stocks')


    def __init__(self, item_name: str, quantity: int, supplier_id: int, unit_cost: float):
        self.item_name = item_name
        self.quantity = quantity
        self.supplier_id = supplier_id
        self.unit_cost = unit_cost

    def receive_stock(self, quantity: int, unit_cost: float) -> None:
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

    def issue_stock(self, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        if quantity > self.quantity:
            raise ValueError("Not enough stock available")
        self.quantity -= quantity

    def get_stock_level(self)-> int:
        """
        Get the stock level of the current stock.

        Returns:
            int: The quantity of the current stock.
        """
        return self.quantity

    def get_total_cost(self)-> float:
        """
        Calculate the total cost of the current stock.

        Returns:
            float: The total cost of the current stock.
        """
        return self.unit_cost * self.quantity

    def change_supplier(self, new_supplier: Supplier) -> None:
        if not isinstance(new_supplier, Supplier):
            raise ValueError("new_supplier must be an instance of Supplier")
        self.supplier = new_supplier

    def get_supplier_details(self) -> str:
        """
        Get the supplier details of the current stock.

        Returns:
            str: The supplier details of the current stock.
        """
        return self.supplier.name if self.supplier else 'No Supplier'
    
def add_supplier(db: Session, name: str):
    supplier = Supplier(name=name)
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    print(f"Supplier {name} added with ID {supplier.id}")

def add_stock(db: Session, item_name: str, quantity: int, supplier_id: int, unit_cost: float):
    stock = STOCK(item_name=item_name, quantity=quantity, supplier_id=supplier_id, unit_cost=unit_cost)
    db.add(stock)
    db.commit()
    db.refresh(stock)
    print(f"Stock {item_name} added with ID {stock.id}")

def receive_stock(db: Session, stock_id: int, quantity: int, unit_cost: float):
    stock = db.query(STOCK).get(stock_id)
    if stock:
        stock.receive_stock(quantity, unit_cost)
        db.commit()
        print(f"Received {quantity} of {stock.item_name} at {unit_cost} each.")
    else:
        print(f"No stock found with ID {stock_id}")

def issue_stock(db: Session, stock_id: int, quantity: int):
    stock = db.query(STOCK).get(stock_id)
    if stock:
        stock.issue_stock(quantity)
        db.commit()
        print(f"Issued {quantity} of {stock.item_name}.")
    else:
        print(f"No stock found with ID {stock_id}")

def list_stocks(db: Session):
    stocks = db.query(STOCK).all()
    for stock in stocks:
        print(f"{stock.item_name}: {stock.quantity} units at {stock.unit_cost} each from Supplier {stock.supplier.name if stock.supplier else 'No Supplier'}")