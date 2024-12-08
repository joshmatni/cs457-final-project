from db import get_connection

def add_transaction(user_id, category_id, transaction_type, amount, date):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
        INSERT INTO transactions (user_id, category_id, transaction_type, amount, transaction_date)
        VALUES (%s, %s, %s, %s, %s)
        """, (user_id, category_id, transaction_type, amount, date))
        conn.commit()
    except:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

def list_transactions(user_id, limit=50):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    SELECT t.transaction_id, c.category_name, t.transaction_type, t.amount, t.transaction_date
    FROM transactions t
    JOIN categories c ON t.category_id = c.category_id
    WHERE t.user_id = %s
    ORDER BY t.transaction_date DESC
    LIMIT %s
    """, (user_id, limit))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def get_spending_summary(user_id):
    # Summarize expenses by category
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    SELECT c.category_name, SUM(t.amount)
    FROM transactions t
    JOIN categories c ON t.category_id = c.category_id
    WHERE t.user_id = %s AND t.transaction_type = 'expense'
    GROUP BY c.category_name
    ORDER BY SUM(t.amount) DESC
    """, (user_id,))
    expenses = cur.fetchall()

    # Summarize income total
    cur.execute("""
    SELECT SUM(amount)
    FROM transactions
    WHERE user_id = %s AND transaction_type = 'income'
    """, (user_id,))
    income = cur.fetchone()[0]

    cur.close()
    conn.close()

    return income if income else 0, expenses
