"""User Data Models - Doctor, Pharmacist, Staff"""

from datetime import datetime
from app.database.connection import db
from app.utils.security import hash_password, verify_password

class User(db.Model):
    """Base User model"""
    
    __tablename__ = 'users'
    
    id = db.Column(db.String(50), primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    role = db.Column(db.String(50), nullable=False)  # doctor, pharmacist, staff
    
    # Status
    active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': role
    }
    
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

class Doctor(User):
    """Doctor user with medical credentials"""
    
    __tablename__ = 'doctors'
    
    id = db.Column(db.String(50), db.ForeignKey('users.id'), primary_key=True)
    license_number = db.Column(db.String(100), unique=True)
    specialization = db.Column(db.String(100))
    department = db.Column(db.String(100))
    
    __mapper_args__ = {
        'polymorphic_identity': 'doctor'
    }

class Pharmacist(User):
    """Pharmacist user"""
    
    __tablename__ = 'pharmacists'
    
    id = db.Column(db.String(50), db.ForeignKey('users.id'), primary_key=True)
    license_number = db.Column(db.String(100), unique=True)
    pharmacy_id = db.Column(db.String(50))
    
    __mapper_args__ = {
        'polymorphic_identity': 'pharmacist'
    }

class Staff(User):
    """Administrative staff user"""
    
    __tablename__ = 'staff'
    
    id = db.Column(db.String(50), db.ForeignKey('users.id'), primary_key=True)
    department = db.Column(db.String(100))
    job_title = db.Column(db.String(100))
    
    __mapper_args__ = {
        'polymorphic_identity': 'staff'
    }
