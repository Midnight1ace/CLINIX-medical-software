"""Alert Data Model"""

from datetime import datetime
from sqlalchemy import String, Text, DateTime, Boolean, Column, ForeignKey
from app.database.connection import Base

class Alert(Base):
    """Patient alert for critical conditions"""

    __tablename__ = 'alerts'

    id = Column(String(50), primary_key=True)
    patient_id = Column(String(50), ForeignKey('patients.id'), nullable=False)

    # Alert details
    alert_type = Column(String(50))  # allergy, drug_interaction, condition, abnormal_result
    severity = Column(String(20))  # critical, high, medium, low
    title = Column(String(255), nullable=False)
    description = Column(Text)

    # Timeline
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = Column(DateTime)

    # Status
    active = Column(Boolean, default=True)
    acknowledged_by = Column(String(50))
    acknowledged_at = Column(DateTime)

    # Reference
    related_record_id = Column(String(50))
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'alert_type': self.alert_type,
            'severity': self.severity,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'active': self.active,
            'severity_numeric': self._severity_to_numeric()
        }
    
    def _severity_to_numeric(self):
        """Convert severity to numeric for sorting"""
        severity_map = {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}
        return severity_map.get(self.severity, 0)
    
    def __repr__(self):
        return f'<Alert {self.id}: {self.title}>'
