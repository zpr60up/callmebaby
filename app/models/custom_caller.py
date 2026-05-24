from .scenario import get_db_connection

class CustomCaller:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        callers = conn.execute('SELECT * FROM custom_callers ORDER BY created_at DESC').fetchall()
        conn.close()
        return [dict(ix) for ix in callers]

    @staticmethod
    def create(caller_name, caller_phone, avatar_path=''):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO custom_callers (caller_name, caller_phone, avatar_path) VALUES (?, ?, ?)',
            (caller_name, caller_phone, avatar_path)
        )
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id
    
    @staticmethod
    def delete(caller_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM custom_callers WHERE id = ?', (caller_id,))
        conn.commit()
        conn.close()
