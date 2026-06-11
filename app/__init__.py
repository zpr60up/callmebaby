
import os
import sqlite3
from flask import Flask

def create_app():
    # Initialize Flask App
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'callmebaby-secret-key-2024')
    
    # Ensure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)
    
    # Register DB teardown
    from app.models.db import close_db
    app.teardown_appcontext(close_db)
    
    # Initialize and Upgrade Database
    init_and_upgrade_db(app.instance_path)
    
    # Register Blueprints
    from app.routes.main import bp as main_bp
    from app.routes.call import call_bp
    from app.routes.scenario_routes import scenario_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(call_bp)
    app.register_blueprint(scenario_bp)
    
    return app

def init_and_upgrade_db(instance_path):
    db_path = os.path.join(instance_path, 'database.db')
    schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'schema.sql')
    
    # Check if DB exists
    db_exists = os.path.exists(db_path)
    
    conn = sqlite3.connect(db_path)
    
    if not db_exists:
        # Create tables from schema.sql
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        print('[Call Me Baby] Database initialized.')
    else:
        # Upgrade database if tables/columns are missing
        try:
            # 1. Ensure recordings table exists
            conn.execute('''
                CREATE TABLE IF NOT EXISTS recordings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    display_name TEXT NOT NULL,
                    created_at TEXT DEFAULT (datetime('now','localtime'))
                );
            ''')
            
            # 2. Ensure description column exists in scenarios
            cursor = conn.execute("PRAGMA table_info(scenarios)")
            columns = [row[1] for row in cursor.fetchall()]
            if 'description' not in columns:
                conn.execute("ALTER TABLE scenarios ADD COLUMN description TEXT;")
                conn.commit()
                print('[Call Me Baby] Database upgraded: added description to scenarios.')
        except Exception as e:
            print(f'[Call Me Baby] Error upgrading database: {e}')
            
    conn.close()

# Expose app at package level
app = create_app()

