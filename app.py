import os
from app import create_app
from app.models.db import init_db

app = create_app()

if __name__ == '__main__':
    db_path = os.path.join(app.instance_path, 'database.db')
    if not os.path.exists(db_path):
        with app.app_context():
            init_db()
            print("[Call Me Baby] Database initialized successfully.")
            
    print("[Call Me Baby] Starting development server on http://127.0.0.1:5000/")
    app.run(debug=True, port=5000)
