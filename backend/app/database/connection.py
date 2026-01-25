"""Database Connection and Initialization"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

class Base(DeclarativeBase):
    pass

def get_database_url():
    """Get database connection string from environment"""
    db_type = os.getenv('DB_TYPE', 'sqlite')

    if db_type == 'sqlite':
        return 'sqlite:///instance/patient_records.db'
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

engine = create_engine(get_database_url(), echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize database"""
    # Import all models to ensure they are registered
    from app.models.patient import Patient
    from app.models.user import User
    from app.models.record import MedicalRecord
    from app.models.alert import Alert

    # Create tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
