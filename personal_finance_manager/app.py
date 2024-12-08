import sys
from datetime import datetime
from tabulate import tabulate
from db import initialize_db
from models.users import create_user, get_user_id
from models.categories import create_category, list_categories, get_category_id
from models.budgets import set_budget, get_budgets
from models.transactions import add_transaction, list_transactions, get_spending_summary
from utils.seed_data import seed_from_csv
try:
    from utils.visualization import plot_expense_breakdown
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

def prompt_for_category():
    """Prompt the user for a category name, allowing them to list or select from existing categories."""
    while True:
        category_name = input("Enter category (or type 'list' to see all categories): ").strip()
        if category_name.lower() == 'list':
            cats = list_categories()
            if not cats:
                print("No categories available yet. Add a transaction with a new category to create one.")
            else:
                headers = ["ID", "Category"]
                print(tabulate(cats, headers=headers))
            continue
        
        if category_name:
            return category_name
        else:
            print("Category name cannot be empty.")

def prompt_for_date(prompt_msg="Enter date (YYYY-MM-DD): "):
    """Prompt the user for a date in YYYY-MM-DD format, re-prompting if invalid."""
    while True:
        date_str = input(prompt_msg).strip()
        try:
            # Validate date format
            datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

def prompt_for_amount(prompt_msg="Enter amount: "):
    """Prompt the user for a numeric amount, re-prompting if invalid."""
    while True:
        amount_str = input(prompt_msg).strip()
        try:
            amount = float(amount_str)
            return amount
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")

def prompt_for_transaction_type():
    """Prompt user for transaction type (income or expense)."""
    while True:
        txn_type = input("Enter transaction type (income/expense): ").strip().lower()
        if txn_type in ['income', 'expense']:
            return txn_type
        else:
            print("Invalid transaction type. Please enter 'income' or 'expense'.")

def prompt_for_category_id(category_name):
    """Ensure category exists or create it, then return its ID."""
    cid = get_category_id(category_name)
    if cid is None:
        # If category doesn't exist, ask user if they want to create it
        choice = input(f"Category '{category_name}' does not exist. Create it? (y/n): ").strip().lower()
        if choice == 'y':
            create_category(category_name)
            cid = get_category_id(category_name)
        else:
            print("Please choose an existing category or create a new one.")
            return None
    return cid

def main():
    initialize_db()

    print("=== Personal Finance Manager ===")
    username = input("Enter your username: ").strip()
    user_id = get_user_id(username)
    if not user_id:
        print("User not found, creating new user.")
        user_id = create_user(username)
    else:
        print(f"Welcome {username}!")

    while True:
        print("\nCommands:")
        print("[1] Add transaction")
        print("[2] List transactions")
        print("[3] Set budget")
        print("[4] View budgets")
        print("[5] View spending summary")
        print("[6] Seed data from CSV")
        print("[7] List categories")
        print("[8] Visualize expenses (requires matplotlib)")
        print("[q] Quit")
        choice = input("Enter command: ").strip()

        if choice == '1':
            # Add transaction
            category_name = prompt_for_category()
            category_id = prompt_for_category_id(category_name)
            if category_id is None:
                # User declined to create a new category and must pick again
                continue

            txn_type = prompt_for_transaction_type()
            amount = prompt_for_amount()
            date_str = prompt_for_date()

            add_transaction(user_id, category_id, txn_type, amount, date_str)
            print("Transaction added.")

        elif choice == '2':
            # List transactions
            txns = list_transactions(user_id)
            if not txns:
                print("No transactions found.")
            else:
                headers = ["ID", "Category", "Type", "Amount", "Date"]
                print(tabulate(txns, headers=headers, floatfmt=".2f"))

        elif choice == '3':
            # Set budget
            category_name = prompt_for_category()
            category_id = prompt_for_category_id(category_name)
            if category_id is None:
                continue

            monthly_limit = prompt_for_amount("Enter monthly limit: ")
            set_budget(user_id, category_id, monthly_limit)
            print("Budget set.")

        elif choice == '4':
            # View budgets
            budgets = get_budgets(user_id)
            if not budgets:
                print("No budgets set.")
            else:
                headers = ["Category", "Monthly Limit"]
                print(tabulate(budgets, headers=headers, floatfmt=".2f"))

        elif choice == '5':
            # View spending summary
            income, expenses = get_spending_summary(user_id)
            print(f"Total Income: {income:.2f}")
            if expenses:
                headers = ["Category", "Total Spent"]
                print(tabulate(expenses, headers=headers, floatfmt=".2f"))
            else:
                print("No expenses recorded.")

        elif choice == '6':
            # Seed data from CSV
            csv_path = input("Enter CSV file path: ").strip()
            try:
                seed_from_csv(user_id, csv_path)
                print("Data seeded successfully.")
            except FileNotFoundError:
                print("File not found. Please check the path and try again.")
            except Exception as e:
                print(f"Error seeding data: {e}")

        elif choice == '7':
            # List categories
            cats = list_categories()
            if not cats:
                print("No categories available yet.")
            else:
                headers = ["ID", "Category"]
                print(tabulate(cats, headers=headers))

        elif choice == '8':
            # Visualize expenses if possible
            if HAS_MATPLOTLIB:
                _, expenses = get_spending_summary(user_id)
                if expenses:
                    plot_expense_breakdown(expenses)
                else:
                    print("No expenses to visualize.")
            else:
                print("matplotlib not installed. Please install to visualize.")

        elif choice.lower() == 'q':
            print("Goodbye!")
            sys.exit(0)

        else:
            print("Invalid command. Please choose from the listed options.")

if __name__ == "__main__":
    main()
