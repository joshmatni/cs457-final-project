import csv
from datetime import datetime
from models.category import Category
from models.transaction import Transaction

def seed_from_csv(user_id, account_id, csv_file):
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            category_name = row['category'].strip()
            Category.create(category_name)  # If already exists, no issue
            cat_id = Category.get_category_id(category_name)
            
            txn_date = row['date']
            # Ensure date is in YYYY-MM-DD
            try:
                dt = datetime.strptime(txn_date, '%Y-%m-%d')
            except ValueError:
                dt = datetime.strptime(txn_date, '%m/%d/%Y')

            transaction_type = row['transaction_type'].strip().lower()
            amount = float(row['amount'])

            Transaction.add_transaction(user_id, account_id, cat_id, transaction_type, amount, dt.date())
