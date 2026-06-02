
import os
from flask import Flask, redirect, url_for

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key-callmebaby'
    
    # Ensure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)
    
    # Register DB teardown
    from app.models.db import close_db
    app.teardown_appcontext(close_db)
    
    # Register Blueprints
    from app.routes.scenario_routes import scenario_bp
    app.register_blueprint(scenario_bp)
    
    # Ensure database is initialized with all tables
    with app.app_context():
        from app.models.db import init_db
        db_path = os.path.join(app.instance_path, 'database.db')
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='scenarios'")
            if not cursor.fetchone():
                init_db()
        except Exception:
            init_db()
        finally:
            conn.close()
            
    @app.route('/')
    def index():
        return redirect(url_for('scenario.index'))
        
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
