from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'fake-call-secret-key-123'
    
    # 註冊 Blueprints
    from app.routes.main import main_bp
    from app.routes.call import call_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(call_bp)
    
    return app
