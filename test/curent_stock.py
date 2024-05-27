#!/usr/bin/python3
import unittest
from current_stock import STOCK

class TestStock(unittest.TestCase):
    def setUp(self):
        self.stock = STOCK("Item", 10, "Supplier", 10.0)

    def test_receive_stock(self):
        self.stock.receive_stock(5, 8.0)
        self.assertEqual(self.stock.quantity, 15)
        self.assertEqual(self.stock.unit_cost, 8.0)

    def test_issue_stock(self):
        self.stock.issue_stock(5)
        self.assertEqual(self.stock.quantity, 5)

    def test_get_stock_level(self):
        self.assertEqual(self.stock.get_stock_level(), 10)

    def test_get_total_cost(self):
        self.assertEqual(self.stock.get_total_cost(), 100.0)

    def test_change_supplier(self):
        self.stock.change_supplier("New Supplier")
        self.assertEqual(self.stock.supplier, "New Supplier")

    def test_get_supplier_details(self):
        self.assertEqual(self.stock.get_supplier_details(), "Supplier")

if __name__ == '__main__':
    unittest.main()