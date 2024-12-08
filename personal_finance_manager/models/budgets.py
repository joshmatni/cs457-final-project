from db import get_connection

def set_budget(user_id, category_id, monthly_limit):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Upsert logic
        cur.execute("""
        INSERT INTO budgets (user_id, category_id, monthly_limit)
        VALUES (%s, %s, %s)
        ON CONFLICT (user_id, category_id)
        DO UPDATE SET monthly_limit = EXCLUDED.monthly_limit
        """, (user_id, category_id, monthly_limit))
        conn.commit()
    except:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

def get_budgets(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    SELECT c.category_name, b.monthly_limit
    FROM budgets b
    JOIN categories c ON b.category_id = c.category_id
    WHERE b.user_id = %s
    """, (user_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
