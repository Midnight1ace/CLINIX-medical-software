"""Medical Record Data Model"""

from datetime import datetime
from app.database.connection import db

class MedicalRecord(db.Model):
    """Patient medical record entry"""
    
    __tablename__ = 'medical_records'
    
    id = db.Column(db.String(50), primary_key=True)
    patient_id = db.Column(db.String(50), db.ForeignKey('patients.id'), nullable=False)
    
    # Record details
    record_type = db.Column(db.String(50))  # diagnosis, treatment, lab_result, imaging, etc.
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    
    # Clinical data
    icd_codes = db.Column(db.Text)  # Comma-separated
    medications = db.Column(db.Text)  # JSON
    findings = db.Column(db.Text)
    recommendations = db.Column(db.Text)
    
    # Timeline
    record_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Source
    source = db.Column(db.String(100))  # clinic, pharmacy, lab, hospital, etc.
    source_document_id = db.Column(db.String(255))
    provider_name = db.Column(db.String(255))
    
    # Status
    verified = db.Column(db.Boolean, default=False)
    is_critical = db.Column(db.Boolean, default=False)
    
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
