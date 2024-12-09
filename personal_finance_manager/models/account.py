from db import Database

class Account:
    def __init__(self, account_id=None, user_id=None, account_name=None):
        self.account_id = account_id
        self.user_id = user_id
        self.account_name = account_name

    @classmethod
    def create(cls, user_id, account_name):
        conn = Database.get_connection()
        cur = conn.cursor()
        account_id = None
        try:
            cur.execute("""
                INSERT INTO accounts (user_id, account_name)
                VALUES (%s, %s) RETURNING account_id
            """, (user_id, account_name))
            account_id = cur.fetchone()[0]
            conn.commit()
        except:
            conn.rollback()
            raise
        finally:
            cur.close()
            conn.close()
        return cls(account_id=account_id, user_id=user_id, account_name=account_name)

    @classmethod
    def list_accounts(cls, user_id):
        conn = Database.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT account_id, account_name FROM accounts WHERE user_id = %s ORDER BY account_name", (user_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [cls(account_id=r[0], user_id=user_id, account_name=r[1]) for r in rows]

    @classmethod
    def get_account_id(cls, user_id, account_name):
        conn = Database.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT account_id FROM accounts WHERE user_id = %s AND account_name = %s",
                    (user_id, account_name))
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result[0] if result else None
