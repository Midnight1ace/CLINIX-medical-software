"""AI Patient Record Intelligence Application"""

from flask import Flask
from app.database.connection import init_db

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    if config_name == 'development':
        from config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    elif config_name == 'production':
        from config import ProductionConfig
        app.config.from_object(ProductionConfig)
    
    # Initialize database
    init_db(app)
    
    # Register blueprints
    from app.api import auth, patients, records, ai_summary, pharmacy, clinic, audit
    app.register_blueprint(auth.bp)
    app.register_blueprint(patients.bp)
    app.register_blueprint(records.bp)
    app.register_blueprint(ai_summary.bp)
    app.register_blueprint(pharmacy.bp)
    app.register_blueprint(clinic.bp)
    app.register_blueprint(audit.bp)
    
    return app
