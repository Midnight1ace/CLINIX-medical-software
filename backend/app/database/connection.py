"""Database Connection and Initialization"""

from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def init_db(app):
    """Initialize database with Flask app"""
    db.init_app(app)
    
    with app.app_context():
        # Import all models
        from app.models import Patient, User, Doctor, Pharmacist, Staff, MedicalRecord, Alert
        from app.services.audit_service import AuditLog
        
        # Create tables
        db.create_all()
        print("Database tables created successfully")

def get_db_connection_string():
    """Get database connection string from environment"""
    db_type = os.getenv('DB_TYPE', 'sqlite')
    
    if db_type == 'sqlite':
        return 'sqlite:///patient_records.db'
    elif db_type == 'postgresql':
        return (
            f"postgresql://{os.getenv('DB_USER')}:"
            f"{os.getenv('DB_PASSWORD')}@"
            f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/"
            f"{os.getenv('DB_NAME')}"
        )
    elif db_type == 'mysql':
        return (
            f"mysql+pymysql://{os.getenv('DB_USER')}:"
            f"{os.getenv('DB_PASSWORD')}@"
            f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/"
            f"{os.getenv('DB_NAME')}"
        )
