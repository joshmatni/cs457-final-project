from db import get_connection

def create_user(username):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING user_id", (username,))
        user_id = cur.fetchone()[0]
        conn.commit()
        return user_id
    except:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

def get_user_id(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users WHERE username = %s", (username,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result[0] if result else None
