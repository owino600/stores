#!/usr/bin/python3
import argparse
from sqlalchemy.orm import sessionmaker
from Storage.db_storage import engine, init_db, SessionLocal
from current_stock import add_stock, receive_stock, issue_stock, list_stocks
from utils import validate_positive
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Advanced Inventory Management CLI")
    subparsers = parser.add_subparsers(dest='command')

    # Add supplier
    parser_add_supplier = subparsers.add_parser('add_supplier', help='Add a new supplier')
    parser_add_supplier.add_argument('name', type=str, help='Name of the supplier')

    # Add stock
    parser_add_stock = subparsers.add_parser('add_stock', help='Add new stock')
    parser_add_stock.add_argument('item_name', type=str, help='Name of the item')
    parser_add_stock.add_argument('quantity', type=validate_positive, help='Quantity of the item')
    parser_add_stock.add_argument('supplier_id', type=int, help='ID of the supplier')
    parser_add_stock.add_argument('unit_cost', type=float, help='Unit cost of the item')

    # Receive stock
    parser_receive_stock = subparsers.add_parser('receive_stock', help='Receive stock')
    parser_receive_stock.add_argument('stock_id', type=int, help='ID of the stock')
    parser_receive_stock.add_argument('quantity', type=validate_positive, help='Quantity to receive')
    parser_receive_stock.add_argument('unit_cost', type=float, help='Unit cost of the stock')

    # Issue stock
    parser_issue_stock = subparsers.add_parser('issue_stock', help='Issue stock')
    parser_issue_stock.add_argument('stock_id', type=int, help='ID of the stock')
    parser_issue_stock.add_argument('quantity', type=validate_positive, help='Quantity to issue')

    # List stocks
    parser_list_stocks = subparsers.add_parser('list_stocks', help='List all stocks')

    args = parser.parse_args()
    db = SessionLocal()

    if args.command == 'add_supplier':
        add_supplier(db, args.name)
    elif args.command == 'add_stock':
        add_stock(db, args.item_name, args.quantity, args.supplier_id, args.unit_cost)
    elif args.command == 'receive_stock':
        receive_stock(db, args.stock_id, args.quantity, args.unit_cost)
    elif args.command == 'issue_stock':
        issue_stock(db, args.stock_id, args.quantity)
    elif args.command == 'list_stocks':
        list_stocks(db)
    else:
        parser.print_help()

if __name__ == '__main__':
    init_db()
    main()