import csv
import datetime

input_file = "PS_20174392719_1491204439457_log.csv"  # raw dataset file
output_file = "processed_transactions.csv"

start_date = datetime.date(2021, 1, 1)

with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = ['date', 'transaction_type', 'category', 'amount']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    
    for row in reader:
        step = int(row['step'])
        txn_type_original = row['type'].strip().upper()
        amount = float(row['amount'])

        # Convert step to a date (assuming each step is 1 day)
        txn_date = start_date + datetime.timedelta(days=(step - 1))

        # Determine transaction_type based on original type
        # CASH_IN is income, everything else is expense:
        if txn_type_original == 'CASH_IN':
            transaction_type = 'income'
        else:
            transaction_type = 'expense'

        # Use the original type as the category
        category = txn_type_original.capitalize()

        # new CSV
        writer.writerow({
            'date': txn_date.strftime('%Y-%m-%d'),
            'transaction_type': transaction_type,
            'category': category,
            'amount': amount
        })

print("Preprocessing complete. The file 'processed_transactions.csv' is ready.")
