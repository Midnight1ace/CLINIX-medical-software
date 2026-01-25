"""Medical Record Data Model"""

from datetime import datetime
from sqlalchemy import String, Text, DateTime, Boolean, Column, ForeignKey
from app.database.connection import Base

class MedicalRecord(Base):
    """Patient medical record entry"""

    __tablename__ = 'medical_records'

    id = Column(String(50), primary_key=True)
    patient_id = Column(String(50), ForeignKey('patients.id'), nullable=False)

    # Record details
    record_type = Column(String(50))  # diagnosis, treatment, lab_result, imaging, etc.
    title = Column(String(255))
    description = Column(Text)

    # Clinical data
    icd_codes = Column(Text)  # Comma-separated
    medications = Column(Text)  # JSON
    findings = Column(Text)
    recommendations = Column(Text)

    # Timeline
    record_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Source
    source = Column(String(100))  # clinic, pharmacy, lab, hospital, etc.
    source_document_id = Column(String(255))
    provider_name = Column(String(255))

    # Status
    verified = Column(Boolean, default=False)
    is_critical = Column(Boolean, default=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'record_type': self.record_type,
            'title': self.title,
            'description': self.description,
            'record_date': self.record_date.isoformat() if self.record_date else None,
            'source': self.source,
            'verified': self.verified,
            'is_critical': self.is_critical
        }
    
    def __repr__(self):
        return f'<MedicalRecord {self.id}: {self.title}>'
