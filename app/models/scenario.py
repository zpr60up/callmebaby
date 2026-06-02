
import sqlite3
import os
from datetime import datetime
from flask import current_app

def get_db_path():
    try:
        # Use Flask's instance path if in app context
        if current_app:
            return os.path.join(current_app.instance_path, 'database.db')
    except RuntimeError:
        pass
    
    # Fallback paths
    paths = [
        os.path.join('instance', 'database.db'),
        os.path.join('database', 'callmebaby.db'),
        'database/callmebaby.db'
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    return 'database/callmebaby.db'

def get_db_connection():
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn

class Scenario:
    def __init__(self, id, title, name, caller_name, caller_phone, phone_number, caller_number, 
                 avatar_path, voice_path, audio_path, audio_file, category, description, is_custom, created_at):
        self.id = id
        self.title = title
        self.name = name
        self.caller_name = caller_name
        self.caller_phone = caller_phone
        self.phone_number = phone_number
        self.caller_number = caller_number
        self.avatar_path = avatar_path
        self.voice_path = voice_path
        self.audio_path = audio_path
        self._audio_file = audio_file
        self.category = category
        self.description = description
        self.is_custom = is_custom
        self.created_at = created_at

    @property
    def audio_file(self):
        val = self._audio_file
        if val and '/' in val:
            return val.split('/')[-1]
        return val

    @audio_file.setter
    def audio_file(self, value):
        self._audio_file = value

    def __getitem__(self, item):
        try:
            return getattr(self, item)
        except AttributeError:
            raise KeyError(item)

    def get(self, item, default=None):
        return getattr(self, item, default)

    def keys(self):
        return ['id', 'title', 'name', 'caller_name', 'caller_phone', 'phone_number', 'caller_number',
                'avatar_path', 'voice_path', 'audio_path', 'audio_file', 'category', 'description',
                'is_custom', 'created_at']

    @staticmethod
    def _row_to_obj(row):
        if row is None:
            return None
        keys = row.keys()
        return Scenario(
            id=row['id'] if 'id' in keys else None,
            title=row['title'] if 'title' in keys else None,
            name=row['name'] if 'name' in keys else None,
            caller_name=row['caller_name'] if 'caller_name' in keys else None,
            caller_phone=row['caller_phone'] if 'caller_phone' in keys else None,
            phone_number=row['phone_number'] if 'phone_number' in keys else None,
            caller_number=row['caller_number'] if 'caller_number' in keys else None,
            avatar_path=row['avatar_path'] if 'avatar_path' in keys else None,
            voice_path=row['voice_path'] if 'voice_path' in keys else None,
            audio_path=row['audio_path'] if 'audio_path' in keys else None,
            audio_file=row['audio_file'] if 'audio_file' in keys else None,
            category=row['category'] if 'category' in keys else None,
            description=row['description'] if 'description' in keys else None,
            is_custom=row['is_custom'] if 'is_custom' in keys else 0,
            created_at=row['created_at'] if 'created_at' in keys else None
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
    def create(cls, title, caller_name, phone_number, description=None, voice_path='/static/audio/family_emergency.mp3', is_custom=True):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO scenarios 
               (title, name, caller_name, caller_phone, phone_number, caller_number, avatar_path, voice_path, audio_path, audio_file, category, description, is_custom)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (
                title,
                title,                  # name
                caller_name,
                phone_number,           # caller_phone
                phone_number,           # phone_number
                phone_number,           # caller_number
                '/static/images/avatar_default.png', # avatar_path
                voice_path,             # voice_path
                voice_path,             # audio_path
                voice_path,             # audio_file
                'custom',               # category
                description,
                1 if is_custom else 0
            )
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

