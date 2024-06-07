#!/usr/bin/python3
import unittest
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from current_stock import Supplier, STOCK, Base
from Storage.db_storage import DB_STORAGE  # Adjust the import according to your file structure

class TestDBStorage(unittest.TestCase):

    def setUp(self):
        """Set up a test database and session"""
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.db_storage = DB_STORAGE()
        self.db_storage._DB_STORAGE__engine = self.engine
        self.db_storage.reload()
        self.db_storage._DB_STORAGE__session = self.session

        self.supplier = Supplier(id=1, name='Test Supplier')
        self.stock = STOCK(item_name='Test Item', quantity=10, supplier_id=1, unit_cost=5.0)
        self.stock.supplier = self.supplier
        self.db_storage.new(self.supplier)
        self.db_storage.new(self.stock)
        self.db_storage.save()

    def tearDown(self):
        """Tear down the test database and session"""
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def test_new(self):
        """Test the new method"""
        supplier = Supplier(id=2, name='New Supplier')
        self.db_storage.new(supplier)
        self.db_storage.save()
        stored_supplier = self.session.query(Supplier).get(2)
        self.assertIsNotNone(stored_supplier)
        self.assertEqual(stored_supplier.name, 'New Supplier')

    def test_save(self):
        """Test the save method"""
        self.stock.quantity = 20
        self.db_storage.save()
        stored_stock = self.session.query(STOCK).get(self.stock.id)
        self.assertEqual(stored_stock.quantity, 20)

    def test_delete(self):
        """Test the delete method"""
        self.db_storage.delete(self.stock)
        self.db_storage.save()
        stored_stock = self.session.query(STOCK).get(self.stock.id)
        self.assertIsNone(stored_stock)

    def test_reload(self):
        """Test the reload method"""
        self.db_storage.close()
        self.db_storage.reload()
        stored_stock = self.db_storage.get('current_stock', self.stock.id)
        self.assertIsNotNone(stored_stock)
        self.assertEqual(stored_stock.item_name, 'Test Item')

    def test_close(self):
        """Test the close method"""
        self.db_storage.close()
        self.assertRaises(sqlalchemy.orm.exc.DetachedInstanceError, self.stock.get_stock_level)

    def test_get(self):
        """Test the get method"""
        stored_stock = self.db_storage.get('current_stock', self.stock.id)
        self.assertIsNotNone(stored_stock)
        self.assertEqual(stored_stock.item_name, 'Test Item')

        stored_supplier = self.db_storage.get('suppliers', self.supplier.id)
        self.assertIsNotNone(stored_supplier)
        self.assertEqual(stored_supplier.name, 'Test Supplier')

        non_existent = self.db_storage.get('current_stock', 999)
        self.assertIsNone(non_existent)

if __name__ == '__main__':
    unittest.main()