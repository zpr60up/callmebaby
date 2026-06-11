import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class Scenario:
    def __init__(self, id, name, caller_name, caller_number, audio_file, is_custom, created_at, description=None):
        self.id = id
        self.name = name
        self.caller_name = caller_name
        self.caller_number = caller_number
        self.audio_file = audio_file
        self.is_custom = is_custom
        self.created_at = created_at
        self.description = description

    @property
    def title(self):
        return self.name

    @title.setter
    def title(self, value):
        self.name = value

    @property
    def phone_number(self):
        return self.caller_number

    @phone_number.setter
    def phone_number(self, value):
        self.caller_number = value

    @property
    def voice_path(self):
        return self.audio_file

    @voice_path.setter
    def voice_path(self, value):
        self.audio_file = value

    def __getitem__(self, item):
        if item == 'title':
            return self.name
        elif item == 'phone_number':
            return self.caller_number
        elif item == 'voice_path':
            return self.audio_file
        try:
            return getattr(self, item)
        except AttributeError:
            raise KeyError(item)

    def get(self, item, default=None):
        if item == 'title':
            return self.name
        elif item == 'phone_number':
            return self.caller_number
        elif item == 'voice_path':
            return self.audio_file
        return getattr(self, item, default)

    def keys(self):
        return ['id', 'name', 'title', 'caller_name', 'caller_number', 'phone_number', 'audio_file', 'voice_path', 'is_custom', 'created_at', 'description']

    @classmethod
    def _row_to_obj(cls, row):
        if row is None:
            return None
        keys = row.keys()
        desc = row['description'] if 'description' in keys else None
        return cls(
            id=row['id'],
            name=row['name'],
            caller_name=row['caller_name'],
            caller_number=row['caller_number'],
            audio_file=row['audio_file'],
            is_custom=row['is_custom'],
            created_at=row['created_at'],
            description=desc
        )

    @classmethod
    def get_all(cls):
        conn = get_db_connection()
        scenarios = conn.execute('SELECT * FROM scenarios').fetchall()
        conn.close()
        return [cls._row_to_obj(row) for row in scenarios]

    @classmethod
    def get_by_id(cls, scenario_id):
        conn = get_db_connection()
        row = conn.execute('SELECT * FROM scenarios WHERE id = ?', (scenario_id,)).fetchone()
        conn.close()
        return cls._row_to_obj(row)

    @classmethod
    def create(cls, name, caller_name, caller_number, description=None, audio_file='/static/audio/family_emergency.mp3', is_custom=True):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO scenarios (name, caller_name, caller_number, description, audio_file, is_custom)
               VALUES (?, ?, ?, ?, ?, ?)''',
            (name, caller_name, caller_number, description, audio_file, 1 if is_custom else 0)
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

