import psycopg2
from psycopg2 import sql

# local PostgreSQL setup
DB_NAME = "personal_finance_db"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"
DB_PORT = 5432

def get_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

def initialize_db():
    # Create tables if not exist
    conn = get_connection()
    cur = conn.cursor()

    # Create users table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL
    );
    """)

    # Create categories table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        category_id SERIAL PRIMARY KEY,
        category_name VARCHAR(255) UNIQUE NOT NULL
    );
    """)

    # Create budgets table
    # user_id, category_id, monthly_limit
    cur.execute("""
    CREATE TABLE IF NOT EXISTS budgets (
        budget_id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
        category_id INT REFERENCES categories(category_id) ON DELETE CASCADE,
        monthly_limit NUMERIC(12, 2)
    );
    """)

    # Create transactions table
    # user_id, category_id, amount (positive=income, negative=expense), date
    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
        category_id INT REFERENCES categories(category_id),
        transaction_type VARCHAR(20) NOT NULL, -- 'income' or 'expense'
        amount NUMERIC(12, 2) NOT NULL,
        transaction_date DATE NOT NULL
    );
    """)

    conn.commit()
    cur.close()
    conn.close()
