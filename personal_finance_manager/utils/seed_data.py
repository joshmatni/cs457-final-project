import csv
from datetime import datetime
from models.categories import create_category, get_category_id
from models.transactions import add_transaction

def seed_from_csv(user_id, csv_file):
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            category_name = row['category'].strip()
            create_category(category_name)
            category_id = get_category_id(category_name)
            
            # Standardize date format to YYYY-MM-DD
            txn_date = row['date']
            try:
                dt = datetime.strptime(txn_date, '%Y-%m-%d')
            except ValueError:
                # Try diff format if needed
                dt = datetime.strptime(txn_date, '%m/%d/%Y')
            
            transaction_type = row['transaction_type'].strip().lower()
            amount = float(row['amount'])

            add_transaction(user_id, category_id, transaction_type, amount, dt.date())
