import os
from flask import Flask

def create_app():
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static'
    )
    app.config['SECRET_KEY'] = 'dev-secret-key-callmebaby'
    
    # Ensure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)
    
    # Register DB teardown
    from app.models.db import close_db
    app.teardown_appcontext(close_db)
    
    # Register Blueprints
    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.routes.call import call_bp
    app.register_blueprint(call_bp)
    
    from app.routes.scenario_routes import scenario_bp
    app.register_blueprint(scenario_bp)
    
    return app
