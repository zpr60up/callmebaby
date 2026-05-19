import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class Scenario:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        scenarios = conn.execute('SELECT * FROM scenarios').fetchall()
        conn.close()
        return [dict(ix) for ix in scenarios]

    @staticmethod
    def get_by_id(scenario_id):
        conn = get_db_connection()
        scenario = conn.execute('SELECT * FROM scenarios WHERE id = ?', (scenario_id,)).fetchone()
        conn.close()
        return dict(scenario) if scenario else None
