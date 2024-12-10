# Joshua Matni
# CS 457 Database Management Systems Final Project!
# Personal Finance Manager

import sys
import os
from tabulate import tabulate
from db import Database
from models.user import User
from models.category import Category
from models.budget import Budget
from models.transaction import Transaction
from models.account import Account
from utils.seed_data import seed_from_csv
try:
    from utils.visualization import plot_expense_breakdown
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
from datetime import datetime

def clear_screen():
    # Clear screen for a cleaner UI
    # Works on most UNIX systems and Windows
    os.system('cls' if os.name == 'nt' else 'clear')

def prompt_for_category():
    while True:
        category_name = input("Enter category (or type 'list' to see all categories, or press enter to go back): ").strip()
        if category_name == '':
            # Return to previous menu
            return None
        if category_name.lower() == 'list':
            cats = Category.list_categories()
            if not cats:
                print("No categories available yet. Add a transaction with a new category to create one.")
            else:
                data = [(c.category_id, c.category_name) for c in cats]
                headers = ["ID", "Category"]
                print(tabulate(data, headers=headers))
            continue
        
        if category_name:
            return category_name
        else:
            print("Category name cannot be empty.")

def prompt_for_date(prompt_msg="Enter date (YYYY-MM-DD or press enter to cancel): "):
    while True:
        date_str = input(prompt_msg).strip()
        if date_str == '':
            return None
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

def prompt_for_amount(prompt_msg="Enter amount (or press enter to cancel): "):
    while True:
        amount_str = input(prompt_msg).strip()
        if amount_str == '':
            return None
        try:
            amt = float(amount_str)
            if amt < 0:
                print("Amount cannot be negative. Please enter a positive value.")
                continue
            return amt
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")

def prompt_for_transaction_type():
    while True:
        txn_type = input("Enter transaction type (income/expense, or press enter to cancel): ").strip().lower()
        if txn_type == '':
            return None
        if txn_type in ['income', 'expense']:
            return txn_type
        else:
            print("Invalid transaction type. Please enter 'income' or 'expense'.")

def prompt_for_category_id(category_name):
    if category_name is None:
        return None
    cid = Category.get_category_id(category_name)
    if cid is None:
        choice = input(f"Category '{category_name}' does not exist. Create it? (y/n): ").strip().lower()
        if choice == 'y':
            if category_name == '':
                print("Category name cannot be empty.")
                return None
            Category.create(category_name)
            cid = Category.get_category_id(category_name)
        else:
            print("Please choose an existing category or create a new one.")
            return None
    return cid

def prompt_for_account(user_id):
    while True:
        account_name = input("Enter account name (or type 'list' to see accounts, press enter to go back): ").strip()
        if account_name == '':
            return None
        if account_name.lower() == 'list':
            accounts = Account.list_accounts(user_id)
            if not accounts:
                print("No accounts available. Create one by entering a new name.")
            else:
                data = [(a.account_id, a.account_name) for a in accounts]
                headers = ["ID", "Account Name"]
                print(tabulate(data, headers=headers))
            continue

        # Check if account exists
        account_id = Account.get_account_id(user_id, account_name)
        if account_id is None:
            choice = input(f"Account '{account_name}' does not exist. Create it? (y/n): ").strip().lower()
            if choice == 'y':
                if account_name == '':
                    print("Account name cannot be empty.")
                    continue
                new_account = Account.create(user_id, account_name)
                return new_account.account_id
            else:
                print("Please select or create an account.")
        else:
            return account_id

def main():
    Database.initialize_db()

    print("=== Personal Finance Manager ===")
    username = input("Enter your username: ").strip()
    if username == '':
        print("Username cannot be empty.")
        sys.exit(1)
    user = User.get_by_username(username)
    if not user:
        print("User not found, creating new user.")
        user = User.create(username)

    while True:
        print("\nCommands:")
        print("[0] Clear Screen")
        print("[1] Add transaction")
        print("[2] List transactions")
        print("[3] Set budget")
        print("[4] View budgets")
        print("[5] View spending summary")
        print("[6] Seed data from CSV")
        print("[7] List categories")
        print("[8] Visualize expenses (requires matplotlib)")
        print("[9] List accounts")
        print("[q] Quit")
        choice = input("Enter command: ").strip()

        if choice == '0':
            clear_screen()

        elif choice == '1':
            account_id = prompt_for_account(user.user_id)
            if account_id is None:
                print("Action cancelled.")
                continue
            category_name = prompt_for_category()
            if category_name is None:
                print("Action cancelled.")
                continue
            category_id = prompt_for_category_id(category_name)
            if category_id is None:
                print("Action cancelled.")
                continue
            txn_type = prompt_for_transaction_type()
            if txn_type is None:
                print("Action cancelled.")
                continue
            amount = prompt_for_amount("Enter amount (or press enter to cancel): ")
            if amount is None:
                print("Action cancelled.")
                continue
            date_str = prompt_for_date()
            if date_str is None:
                print("Action cancelled.")
                continue

            Transaction.add_transaction(user.user_id, account_id, category_id, txn_type, amount, date_str)
            print("Transaction added.")
            print("-" * 50)

        elif choice == '2':
            txns = Transaction.list_transactions(user.user_id)
            if not txns:
                print("No transactions found.")
            else:
                headers = ["ID", "Category", "Type", "Amount", "Date", "Account"]
                print(tabulate(txns, headers=headers, floatfmt=".2f"))
            input("Press Enter to return to the main menu...")
            print("-" * 50)

        elif choice == '3':
            category_name = prompt_for_category()
            if category_name is None:
                print("Action cancelled.")
                continue
            category_id = prompt_for_category_id(category_name)
            if category_id is None:
                print("Action cancelled.")
                continue
            monthly_limit = prompt_for_amount("Enter monthly limit: ")
            if monthly_limit is None:
                print("Action cancelled.")
                continue
            Budget.set_budget(user.user_id, category_id, monthly_limit)
            print("Budget set.")
            print("-" * 50)

        elif choice == '4':
            budgets = Budget.get_budgets(user.user_id)
            if not budgets:
                print("No budgets set.")
            else:
                headers = ["Category", "Monthly Limit"]
                print(tabulate(budgets, headers=headers, floatfmt=".2f"))
            input("Press Enter to return to the main menu...")
            print("-" * 50)

        elif choice == '5':
            income, expenses = Transaction.get_spending_summary(user.user_id)
            print(f"Total Income: {income:.2f}")
            if expenses:
                headers = ["Category", "Total Spent"]
                print(tabulate(expenses, headers=headers, floatfmt=".2f"))
            else:
                print("No expenses recorded.")
            input("Press Enter to return to the main menu...")
            print("-" * 50)

        elif choice == '6':
            accounts = Account.list_accounts(user.user_id)
            if not accounts:
                print("No accounts available. You must have at least one account to seed data into.")
                acc_name = input("Create an account name (or press enter to cancel): ").strip()
                if acc_name == '':
                    print("Action cancelled.")
                    continue
                acc = Account.create(user.user_id, acc_name)
                account_id = acc.account_id
            else:
                account_id = prompt_for_account(user.user_id)
                if account_id is None:
                    print("Action cancelled.")
                    continue

            csv_path = input("Enter CSV file path (or press enter to cancel): ").strip()
            if csv_path == '':
                print("Action cancelled.")
                continue
            if not os.path.exists(csv_path):
                print("File not found. Please check the path and try again.")
                continue
            try:
                seed_from_csv(user.user_id, account_id, csv_path)
                print("Data seeded successfully.")
            except FileNotFoundError:
                print("File not found. Please check the path and try again.")
            except Exception as e:
                print(f"Error seeding data: {e}")
            input("Press Enter to return to the main menu...")
            print("-" * 50)

        elif choice == '7':
            cats = Category.list_categories()
            if not cats:
                print("No categories available yet.")
            else:
                data = [(c.category_id, c.category_name) for c in cats]
                headers = ["ID", "Category"]
                print(tabulate(data, headers=headers))
            input("Press Enter to return to the main menu...")
            print("-" * 50)

        elif choice == '8':
            if HAS_MATPLOTLIB:
                _, expenses = Transaction.get_spending_summary(user.user_id)
                if expenses:
                    plot_expense_breakdown(expenses)
                else:
                    print("No expenses to visualize.")
            else:
                print("matplotlib not installed. Please install to visualize.")
            input("Press Enter to return to the main menu...")
            print("-" * 50)

        elif choice == '9':
            accounts = Account.list_accounts(user.user_id)
            if not accounts:
                print("No accounts available.")
            else:
                data = [(a.account_id, a.account_name) for a in accounts]
                headers = ["ID", "Account Name"]
                print(tabulate(data, headers=headers))
            input("Press Enter to return to the main menu...")
            print("-" * 50)

        elif choice.lower() == 'q':
            print("Goodbye!")
            sys.exit(0)

        else:
            print("Invalid command. Please choose from the listed options.")
            print("-" * 50)


if __name__ == "__main__":
    main()
