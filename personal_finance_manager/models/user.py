from db import Database

class User:
    def __init__(self, user_id=None, username=None):
        self.user_id = user_id
        self.username = username

    @classmethod
    def create(cls, username):
        conn = Database.get_connection()
        cur = conn.cursor()
        user_id = None
        try:
            cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING user_id", (username,))
            user_id = cur.fetchone()[0]
            conn.commit()
        except:
            conn.rollback()
            raise
        finally:
            cur.close()
            conn.close()
        return cls(user_id=user_id, username=username)

    @classmethod
    def get_by_username(cls, username):
        conn = Database.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT user_id, username FROM users WHERE username = %s", (username,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        if result:
            return cls(user_id=result[0], username=result[1])
        return None
