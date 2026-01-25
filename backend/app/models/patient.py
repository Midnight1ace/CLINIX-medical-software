"""Patient Data Model"""

from datetime import datetime
from sqlalchemy import String, Date, Boolean, Text, Column, DateTime
from app.database.connection import Base

class Patient(Base):
    """Patient profile and basic information"""
    
    __tablename__ = 'patients'
    
    __tablename__ = 'patients'

    id = Column(String(50), primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(10))
    email = Column(String(120), unique=True)
    phone = Column(String(20))

    # Address
    address_line1 = Column(String(255))
    address_line2 = Column(String(255))
    city = Column(String(100))
    state = Column(String(50))
    postal_code = Column(String(20))
    country = Column(String(100))

    # Medical info
    blood_type = Column(String(10))
    allergies = Column(Text)
    chronic_conditions = Column(Text)
    emergency_contact = Column(String(255))
    emergency_contact_phone = Column(String(20))

    # Additional fields for API compliance
    national_id = Column(String(50))

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    active = Column(Boolean, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'gender': self.gender,
            'email': self.email,
            'phone': self.phone,
            'blood_type': self.blood_type,
            'allergies': self.allergies,
            'chronic_conditions': self.chronic_conditions
        }
    
    def __repr__(self):
        return f'<Patient {self.id}: {self.first_name} {self.last_name}>'
