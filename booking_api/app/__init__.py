import os
from flask import Flask
from flask_migrate import Migrate

from .models import db
from .config import config

migrate = Migrate()

def create_app(config_name=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Determine the configuration to use
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from .routes import api
    app.register_blueprint(api)
    
    @app.route('/')
    def index():
        return {
            "message": "Welcome to the Bitcube Room Booking API",
            "version": "1.0.0",
            "documentation": "/api/docs"
        }
    
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    return app
