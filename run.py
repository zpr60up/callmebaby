import sqlite3
import os
from flask import Flask

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.secret_key = 'your_secret_key_here'

# Database configuration
DATABASE = os.path.join(app.instance_path, 'database.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)
        
    with app.app_context():
        db = get_db_connection()
        with open('database/schema.sql', 'r', encoding='utf-8') as f:
            db.cursor().executescript(f.read())
            
        # Insert default scenarios if the table is empty
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM scenarios")
        count = cursor.fetchone()[0]
        
        if count == 0:
            default_scenarios = [
                ('家庭急事', '爸爸', '0912-345-678', '/static/images/avatar_dad.png', '', 'emergency'),
                ('老闆奪命連環call', '老闆', '0988-888-888', '/static/images/avatar_boss.png', '', 'work'),
                ('快遞取件', '黑貓宅急便', '0933-222-111', '/static/images/avatar_delivery.png', '', 'delivery'),
            ]
            cursor.executemany("INSERT INTO scenarios (title, caller_name, caller_phone, avatar_path, audio_path, category) VALUES (?, ?, ?, ?, ?, ?)", default_scenarios)
            
        db.commit()
        db.close()
        print("Database initialized.")

# Import routes
from app.routes.main import bp as main_bp
app.register_blueprint(main_bp)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
