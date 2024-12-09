from db import Database

class Category:
    def __init__(self, category_id=None, category_name=None):
        self.category_id = category_id
        self.category_name = category_name

    @classmethod
    def create(cls, category_name):
        conn = Database.get_connection()
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

    @classmethod
    def get_category_id(cls, category_name):
        conn = Database.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT category_id FROM categories WHERE category_name = %s", (category_name,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result[0] if result else None

    @classmethod
    def list_categories(cls):
        conn = Database.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT category_id, category_name FROM categories ORDER BY category_name")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [cls(category_id=r[0], category_name=r[1]) for r in rows]
