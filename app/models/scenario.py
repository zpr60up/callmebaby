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

    @staticmethod
    def create(title, caller_name, phone_number, description, voice_path=''):
        db = get_db()
        cursor = db.execute(
            'INSERT INTO scenarios (title, caller_name, phone_number, description, voice_path) VALUES (?, ?, ?, ?, ?)',
            (title, caller_name, phone_number, description, voice_path)
        )
        db.commit()
        return cursor.lastrowid
