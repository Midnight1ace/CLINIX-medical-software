"""Alert Data Model"""

from datetime import datetime
from app.database.connection import db

class Alert(db.Model):
    """Patient alert for critical conditions"""
    
    __tablename__ = 'alerts'
    
    id = db.Column(db.String(50), primary_key=True)
    patient_id = db.Column(db.String(50), db.ForeignKey('patients.id'), nullable=False)
    
    # Alert details
    alert_type = db.Column(db.String(50))  # allergy, drug_interaction, condition, abnormal_result
    severity = db.Column(db.String(20))  # critical, high, medium, low
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    
    # Timeline
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    
    # Status
    active = db.Column(db.Boolean, default=True)
    acknowledged_by = db.Column(db.String(50))
    acknowledged_at = db.Column(db.DateTime)
    
    # Reference
    related_record_id = db.Column(db.String(50))
    
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
