import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class Scenario:
    def __init__(self, id, name, caller_name, caller_number, avatar_path, audio_file, description, category, is_custom, created_at):
        self.id = id
        self.name = name
        self.caller_name = caller_name
        self.caller_number = caller_number
        self.avatar_path = avatar_path
        self.audio_file = audio_file
        self.description = description
        self.category = category
        self.is_custom = is_custom
        self.created_at = created_at

    def __getitem__(self, key):
        mapping = {
            'id': self.id,
            'name': self.name,
            'title': self.name,
            'caller_name': self.caller_name,
            'caller_number': self.caller_number,
            'caller_phone': self.caller_number,
            'phone_number': self.caller_number,
            'avatar_path': self.avatar_path,
            'audio_file': self.audio_file,
            'audio_path': self.audio_file,
            'voice_path': self.audio_file,
            'description': self.description,
            'category': self.category,
            'is_custom': self.is_custom,
            'created_at': self.created_at
        }
        return mapping.get(key)

    @property
    def title(self):
        return self.name

    @property
    def caller_phone(self):
        return self.caller_number

    @property
    def phone_number(self):
        return self.caller_number

    @property
    def audio_path(self):
        return self.audio_file

    @property
    def voice_path(self):
        return self.audio_file

    @staticmethod
    def _row_to_obj(row):
        if row is None:
            return None
        return Scenario(
            id=row['id'],
            name=row['name'],
            caller_name=row['caller_name'],
            caller_number=row['caller_number'],
            avatar_path=row['avatar_path'],
            audio_file=row['audio_file'],
            description=row['description'],
            category=row['category'],
            is_custom=row['is_custom'],
            created_at=row['created_at']
        )

    @classmethod
    def get_all(cls):
        conn = get_db_connection()
        scenarios = conn.execute('SELECT * FROM scenarios ORDER BY created_at DESC').fetchall()
        conn.close()
        return [cls._row_to_obj(row) for row in scenarios]

    @classmethod
    def get_by_id(cls, scenario_id):
        conn = get_db_connection()
        row = conn.execute('SELECT * FROM scenarios WHERE id = ?', (scenario_id,)).fetchone()
        conn.close()
        return cls._row_to_obj(row)

    @classmethod
    def create(cls, name, caller_name, caller_number, audio_file='', description='', category='default', is_custom=True):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO scenarios (name, caller_name, caller_number, audio_file, description, category, is_custom) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (name, caller_name, caller_number, audio_file, description, category, is_custom)
        )
        conn.commit()
        scenario_id = cursor.lastrowid
        conn.close()
        return cls.get_by_id(scenario_id)

    @classmethod
    def delete(cls, scenario_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM scenarios WHERE id = ?', (scenario_id,))
        conn.commit()
        conn.close()
