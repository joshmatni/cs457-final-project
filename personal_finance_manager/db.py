import psycopg2
from psycopg2 import sql

class Database:
    DB_NAME = "personal_finance_db"
    DB_USER = "postgres"
    DB_PASSWORD = "postgres"
    DB_HOST = "localhost"
    DB_PORT = 5432

    @classmethod
    def get_connection(cls):
        return psycopg2.connect(
            dbname=cls.DB_NAME,
            user=cls.DB_USER,
            password=cls.DB_PASSWORD,
            host=cls.DB_HOST,
            port=cls.DB_PORT
        )

    @classmethod
    def initialize_db(cls):
        conn = cls.get_connection()
        cur = conn.cursor()

        # Create users table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL
        );
        """)

        # Create accounts table (new)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            account_id SERIAL PRIMARY KEY,
            user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
            account_name VARCHAR(255) NOT NULL
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
        cur.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            budget_id SERIAL PRIMARY KEY,
            user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
            category_id INT REFERENCES categories(category_id) ON DELETE CASCADE,
            monthly_limit NUMERIC(12, 2)
        );
        """)

        # Create transactions table with account_id reference
        cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id SERIAL PRIMARY KEY,
            user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
            account_id INT REFERENCES accounts(account_id) ON DELETE CASCADE,
            category_id INT REFERENCES categories(category_id),
            transaction_type VARCHAR(20) NOT NULL, -- 'income' or 'expense'
            amount NUMERIC(12, 2) NOT NULL,
            transaction_date DATE NOT NULL
        );
        """)

        conn.commit()
        cur.close()
        conn.close()
