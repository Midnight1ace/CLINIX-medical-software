"""Audit Service - Compliance and access logging"""

from app.database.connection import db
from app.utils.logging import log_info, log_error
from datetime import datetime
from uuid import uuid4

class AuditLog(db.Model):
    """Audit log for compliance tracking"""
    
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.String(50), primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    patient_id = db.Column(db.String(50), nullable=False)
    action = db.Column(db.String(100), nullable=False)  # view, edit, export, etc.
    details = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(50))

def log_access(patient_id, user_id, access_type='view', details=None):
    """Log user access to patient record"""
    try:
        audit_log = AuditLog(
            id=str(uuid4()),
            user_id=user_id,
            patient_id=patient_id,
            action=access_type,
            details=details
        )
        
        db.session.add(audit_log)
        db.session.commit()
        
        log_info(f"Audit log: User {user_id} {access_type} patient {patient_id}")
        return True
    except Exception as e:
        log_error(f"Error logging access: {str(e)}")
        db.session.rollback()
        return False

def get_audit_logs(patient_id=None, user_id=None, days=30):
    """Retrieve audit logs with filters"""
    try:
        query = AuditLog.query
        
        if patient_id:
            query = query.filter_by(patient_id=patient_id)
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        logs = query.order_by(AuditLog.timestamp.desc()).all()
        
        return [{
            'id': log.id,
            'user_id': log.user_id,
            'patient_id': log.patient_id,
            'action': log.action,
            'details': log.details,
            'timestamp': log.timestamp.isoformat() if log.timestamp else None
        } for log in logs]
    except Exception as e:
        log_error(f"Error retrieving audit logs: {str(e)}")
        return []

def export_logs(start_date=None, end_date=None):
    """Export audit logs for compliance reporting"""
    # TODO: Implement CSV/Excel export
    pass
