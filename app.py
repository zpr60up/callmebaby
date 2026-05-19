
import os
import sqlite3
from app import create_app

app = create_app()

def init_db():
    db_path = 'database/callmebaby.db'
    schema_path = 'database/schema.sql'
    
    if not os.path.exists('database'):
        os.makedirs('database')
        
    # Check if database already has scenarios
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='scenarios'")
    table_exists = cursor.fetchone()
    
    if not table_exists:
        print("Initializing database...")
        with open(schema_path, 'r', encoding='utf-8') as f:
            cursor.executescript(f.read())
        conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
