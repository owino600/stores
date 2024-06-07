#!/usr/bin/python3
import unittest
from unittest.mock import patch, MagicMock
import sys
from cli import main  # Adjust the import according to your file structure

class TestCLI(unittest.TestCase):

    @patch('cli_script.SessionLocal')
    def test_add_supplier(self, mock_session):
        db = mock_session.return_value
        db.commit = MagicMock()
        testargs = ["cli_script.py", "add_supplier", "Test Supplier"]
        with patch.object(sys, 'argv', testargs):
            main()
        db.add.assert_called()
        db.commit.assert_called()

    @patch('cli_script.SessionLocal')
    def test_add_stock(self, mock_session):
        db = mock_session.return_value
        db.commit = MagicMock()
        testargs = ["cli_script.py", "add_stock", "Test Item", "10", "1", "5.0"]
        with patch.object(sys, 'argv', testargs):
            main()
        db.add.assert_called()
        db.commit.assert_called()

    @patch('cli_script.SessionLocal')
    def test_receive_stock(self, mock_session):
        db = mock_session.return_value
        db.commit = MagicMock()
        testargs = ["cli_script.py", "receive_stock", "1", "5", "4.0"]
        with patch.object(sys, 'argv', testargs):
            main()
        db.commit.assert_called()

    @patch('cli_script.SessionLocal')
    def test_issue_stock(self, mock_session):
        db = mock_session.return_value
        db.commit = MagicMock()
        testargs = ["cli_script.py", "issue_stock", "1", "5"]
        with patch.object(sys, 'argv', testargs):
            main()
        db.commit.assert_called()

    @patch('cli_script.SessionLocal')
    def test_list_stocks(self, mock_session):
        db = mock_session.return_value
        db.commit = MagicMock()
        testargs = ["cli_script.py", "list_stocks"]
        with patch.object(sys, 'argv', testargs):
            main()
        db.query.assert_called()

if __name__ == '__main__':
    unittest.main()