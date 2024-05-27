#!/usr/bin/python3
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from current_stock import Base, STOCK, Supplier

class TestStock(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        # Create a supplier instance
        self.supplier = Supplier(name="Supplier")
        self.session.add(self.supplier)
        self.session.commit()
        
        self.stock = STOCK("Item", 10, "Supplier", 10.0)
        self.session.add(self.stock)
        self.session.commit()

    def test_receive_stock(self):
        self.stock.receive_stock(5, 8.0)
        self.session.commit()
        self.assertEqual(self.stock.quantity, 15)
        self.assertEqual(self.stock.unit_cost, 8.0)

    def test_issue_stock(self):
        self.stock.issue_stock(5)
        self.session.commit()
        self.assertEqual(self.stock.quantity, 5)

    def test_get_stock_level(self):
        self.assertEqual(self.stock.get_stock_level(), 10)

    def test_get_total_cost(self):
        self.assertEqual(self.stock.get_total_cost(), 100.0)

    def test_change_supplier(self):
        new_supplier = Supplier(name="New Supplier")
        self.session.add(new_supplier)
        self.session.commit()
        self.stock.change_supplier(new_supplier)
        self.session.commit()
        self.assertEqual(self.stock.supplier.name, "New Supplier")
    def test_get_supplier_details(self):
        self.assertEqual(self.stock.get_supplier_details(), "No Supplier")

if __name__ == '__main__':
    unittest.main()