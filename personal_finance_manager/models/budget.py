from db import Database

class Budget:
    def __init__(self, budget_id=None, user_id=None, category_id=None, monthly_limit=None):
        self.budget_id = budget_id
        self.user_id = user_id
        self.category_id = category_id
        self.monthly_limit = monthly_limit

    @classmethod
    def set_budget(cls, user_id, category_id, monthly_limit):
        conn = Database.get_connection()
        cur = conn.cursor()
        try:
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

    @classmethod
    def get_budgets(cls, user_id):
        conn = Database.get_connection()
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
