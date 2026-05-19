from app.models.db import get_db

class Scenario:
    @staticmethod
    def get_all():
        db = get_db()
        return db.execute('SELECT * FROM scenarios ORDER BY id ASC').fetchall()

    @staticmethod
    def get_by_id(id):
        db = get_db()
        return db.execute('SELECT * FROM scenarios WHERE id = ?', (id,)).fetchone()
