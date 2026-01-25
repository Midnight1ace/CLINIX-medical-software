"""User Data Models - Doctor, Pharmacist, Staff"""

from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, Column
from app.database.connection import Base
from app.utils.security import hash_password, verify_password

class User(Base):
    """Base User model"""
    
    __tablename__ = 'users'
    
    __tablename__ = 'users'

    id = Column(String(50), primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    role = Column(String(50), nullable=False)  # doctor, pharmacist, staff

    # Status
    active = Column(Boolean, default=True)
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    # Simplified - no inheritance for now
    
    def set_password(self, password):
        """Hash and store password"""
        self.password_hash = hash_password(password)
    
    def check_password(self, password):
        """Verify password"""
        return verify_password(password, self.password_hash)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'active': self.active
        }

# Simplified user model - subclasses removed for now
