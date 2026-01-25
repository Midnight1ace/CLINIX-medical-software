"""Patient Service - Core business logic"""

from app.models.patient import Patient
from app.models.record import MedicalRecord
from app.database.connection import db
from app.utils.logging import log_info, log_error

def search_patients(query):
    """Search for patients by name or ID"""
    try:
        # Search by patient ID, first name, or last name
        results = Patient.query.filter(
            db.or_(
                Patient.id.ilike(f'%{query}%'),
                Patient.first_name.ilike(f'%{query}%'),
                Patient.last_name.ilike(f'%{query}%'),
                Patient.email.ilike(f'%{query}%')
            )
        ).filter(Patient.active == True).limit(20).all()
        
        log_info(f"Patient search for '{query}' returned {len(results)} results")
        return [p.to_dict() for p in results]
    except Exception as e:
        log_error(f"Error searching patients: {str(e)}")
        return []

def get_patient_snapshot(patient_id):
    """Get patient snapshot for main view - current critical data"""
    try:
        patient = Patient.query.filter_by(id=patient_id, active=True).first()
        
        if not patient:
            return None
        
        # Get recent critical alerts
        alerts = get_patient_alerts(patient_id, limit=5)
        
        # Get recent records
        recent_records = get_recent_records(patient_id, limit=10)
        
        snapshot = {
            'patient': patient.to_dict(),
            'alerts': alerts,
            'recent_records': recent_records,
            'generated_at': db.func.now()
        }
        
        return snapshot
    except Exception as e:
        log_error(f"Error getting patient snapshot: {str(e)}")
        return None

def get_patient_alerts(patient_id, limit=10):
    """Get patient's active alerts"""
    try:
        from app.models.alert import Alert
        
        alerts = Alert.query.filter_by(
            patient_id=patient_id,
            active=True
        ).order_by(Alert.created_at.desc()).limit(limit).all()
        
        return [a.to_dict() for a in alerts]
    except Exception as e:
        log_error(f"Error getting patient alerts: {str(e)}")
        return []

def get_recent_records(patient_id, limit=10):
    """Get recent medical records for patient"""
    try:
        records = MedicalRecord.query.filter_by(
            patient_id=patient_id
        ).order_by(MedicalRecord.record_date.desc()).limit(limit).all()
        
        return [r.to_dict() for r in records]
    except Exception as e:
        log_error(f"Error getting recent records: {str(e)}")
        return []

def get_patient_history(patient_id):
    """Get full patient history timeline"""
    try:
        records = MedicalRecord.query.filter_by(
            patient_id=patient_id
        ).order_by(MedicalRecord.record_date.desc()).all()
        
        return [r.to_dict() for r in records]
    except Exception as e:
        log_error(f"Error getting patient history: {str(e)}")
        return []

def get_full_record(patient_id):
    """Get complete patient record with all details"""
    try:
        patient = Patient.query.filter_by(id=patient_id, active=True).first()
        
        if not patient:
            return None
        
        records = MedicalRecord.query.filter_by(patient_id=patient_id).all()
        alerts = get_patient_alerts(patient_id)
        
        full_record = {
            'patient': patient.to_dict(),
            'medical_records': [r.to_dict() for r in records],
            'alerts': alerts
        }
        
        return full_record
    except Exception as e:
        log_error(f"Error getting full record: {str(e)}")
        return None
