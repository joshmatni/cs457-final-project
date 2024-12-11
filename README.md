# cs457-final-project
Database Management Systems Final project

# Personal Finance Manager

A Python-based CLI application to manage personal finances, including transactions, budgets, and spending summaries. It uses PostgreSQL as the backend database.

## Features

- **Add Transactions:** Record income and expenses.
- **Set Budgets:** Define monthly spending limits for categories.
- **View Budgets:** Check current budget allocations.
- **Spending Summary:** Get an overview of total income and expenses by category.
- **Seed Data:** Populate the database with sample data from CSV files.
- **List Categories & Accounts:** View all available categories and accounts.
- **Visualize Expenses:** Generate expense visualizations (requires `matplotlib`).

## Requirements

- **Python 3.6+**
- **PostgreSQL 17.x**
- **Python Packages:**
  - `psycopg2`
  - `matplotlib` (optional, for visualizations)

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/personal_finance_manager.git
   cd personal_finance_manager
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Setup:**
   
   Initialize PostgreSQL Database:
   ```bash
   # Switch to postgres user
   sudo su - postgres

   # Create database
   createdb personal_finance_db

   # Exit postgres user shell
   exit
   ```

4. **Run Application:**
   ```bash
   python3 app.py
   ```