"""Alert Service - Alert detection and management"""

from app.models.alert import Alert
from app.models.patient import Patient
from app.database.connection import db
from app.utils.logging import log_info, log_error
from datetime import datetime

def check_allergies(patient_id, medication_name):
    """Check medication against patient allergies"""
    try:
        patient = Patient.query.filter_by(id=patient_id).first()
        
        if not patient or not patient.allergies:
            return None
        
        # Check if medication is in allergies
        if medication_name.lower() in patient.allergies.lower():
            alert = create_alert(
                patient_id=patient_id,
                alert_type='allergy',
                severity='critical',
                title=f'Allergy Alert: {medication_name}',
                description=f'Patient has documented allergy to {medication_name}'
            )
            return alert
        
        return None
    except Exception as e:
        log_error(f"Error checking allergies: {str(e)}")
        return None

def check_drug_interactions(patient_id, medications_list):
    """Check for potential drug interactions"""
    # TODO: Implement interaction checking with drug database
    pass

def check_abnormal_results(patient_id, test_results):
    """Check for abnormal lab/imaging results"""
    # TODO: Implement result analysis
    pass

def create_alert(patient_id, alert_type, severity, title, description, related_record_id=None):
    """Create a new alert"""
    try:
        from uuid import uuid4
        
        alert = Alert(
            id=str(uuid4()),
            patient_id=patient_id,
            alert_type=alert_type,
            severity=severity,
            title=title,
            description=description,
            related_record_id=related_record_id,
            active=True
        )
        
        db.session.add(alert)
        db.session.commit()
        
        log_info(f"Created {severity} alert for patient {patient_id}: {title}")
        return alert.to_dict()
    except Exception as e:
        log_error(f"Error creating alert: {str(e)}")
        db.session.rollback()
        return None

def resolve_alert(alert_id, resolved_by):
    """Resolve/acknowledge an alert"""
    try:
        alert = Alert.query.filter_by(id=alert_id).first()
        
        if not alert:
            return None
        
        alert.active = False
        alert.resolved_at = datetime.utcnow()
        alert.acknowledged_by = resolved_by
        alert.acknowledged_at = datetime.utcnow()
        
        db.session.commit()
        log_info(f"Resolved alert {alert_id}")
        return alert.to_dict()
    except Exception as e:
        log_error(f"Error resolving alert: {str(e)}")
        db.session.rollback()
        return None

def get_patient_critical_alerts(patient_id):
    """Get critical alerts for patient"""
    try:
        alerts = Alert.query.filter(
            Alert.patient_id == patient_id,
            Alert.severity == 'critical',
            Alert.active == True
        ).all()
        
        return [a.to_dict() for a in alerts]
    except Exception as e:
        log_error(f"Error getting critical alerts: {str(e)}")
        return []
