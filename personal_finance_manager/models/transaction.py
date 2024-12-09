from db import Database

class Transaction:
    def __init__(self, transaction_id=None, user_id=None, account_id=None, category_id=None,
                 transaction_type=None, amount=None, transaction_date=None):
        self.transaction_id = transaction_id
        self.user_id = user_id
        self.account_id = account_id
        self.category_id = category_id
        self.transaction_type = transaction_type
        self.amount = amount
        self.transaction_date = transaction_date

    @classmethod
    def add_transaction(cls, user_id, account_id, category_id, transaction_type, amount, date):
        conn = Database.get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
            INSERT INTO transactions (user_id, account_id, category_id, transaction_type, amount, transaction_date)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, (user_id, account_id, category_id, transaction_type, amount, date))
            conn.commit()
        except:
            conn.rollback()
            raise
        finally:
            cur.close()
            conn.close()

    @classmethod
    def list_transactions(cls, user_id, limit=50):
        conn = Database.get_connection()
        cur = conn.cursor()
        cur.execute("""
        SELECT t.transaction_id, c.category_name, t.transaction_type, t.amount, t.transaction_date, a.account_name
        FROM transactions t
        JOIN categories c ON t.category_id = c.category_id
        JOIN accounts a ON t.account_id = a.account_id
        WHERE t.user_id = %s
        ORDER BY t.transaction_date DESC
        LIMIT %s
        """, (user_id, limit))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    @classmethod
    def get_spending_summary(cls, user_id):
        conn = Database.get_connection()
        cur = conn.cursor()
        # Income total
        cur.execute("""
        SELECT SUM(amount)
        FROM transactions
        WHERE user_id = %s AND transaction_type = 'income'
        """, (user_id,))
        income = cur.fetchone()[0]

        # Expenses by category
        cur.execute("""
        SELECT c.category_name, SUM(t.amount)
        FROM transactions t
        JOIN categories c ON t.category_id = c.category_id
        WHERE t.user_id = %s AND t.transaction_type = 'expense'
        GROUP BY c.category_name
        ORDER BY SUM(t.amount) DESC
        """, (user_id,))
        expenses = cur.fetchall()

        cur.close()
        conn.close()

        return (income if income else 0, expenses)
