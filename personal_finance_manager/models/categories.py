from db import get_connection

def create_category(category_name):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO categories (category_name) VALUES (%s) ON CONFLICT DO NOTHING", (category_name,))
        conn.commit()
    except:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

def get_category_id(category_name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT category_id FROM categories WHERE category_name = %s", (category_name,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result[0] if result else None

def list_categories():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT category_id, category_name FROM categories ORDER BY category_name")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
