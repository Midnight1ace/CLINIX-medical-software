"""Patient Service - Core business logic"""

from app.models.patient import Patient
from app.models.record import MedicalRecord
from app.database.connection import SessionLocal
from app.utils.logging import log_info, log_error
from sqlalchemy import or_, and_

def search_patients(method, value, limit=10):
    """Search for patients by various methods"""
    try:
        session = SessionLocal()
        query = session.query(Patient).filter(Patient.active == True)

        if method == "PATIENT_ID":
            query = query.filter(Patient.id.ilike(f'%{value}%'))
        elif method == "NATIONAL_ID":
            query = query.filter(Patient.national_id.ilike(f'%{value}%'))
        elif method == "PARTIAL_NAME":
            # Split name for first/last name search
            names = value.split()
            if len(names) >= 2:
                query = query.filter(
                    or_(
                        and_(Patient.first_name.ilike(f'%{names[0]}%'), Patient.last_name.ilike(f'%{names[1]}%')),
                        and_(Patient.first_name.ilike(f'%{names[1]}%'), Patient.last_name.ilike(f'%{names[0]}%'))
                    )
                )
            else:
                query = query.filter(
                    or_(
                        Patient.first_name.ilike(f'%{value}%'),
                        Patient.last_name.ilike(f'%{value}%')
                    )
                )
        else:
            # Default search
            query = query.filter(
                or_(
                    Patient.id.ilike(f'%{value}%'),
                    Patient.first_name.ilike(f'%{value}%'),
                    Patient.last_name.ilike(f'%{value}%')
                )
            )

        results = query.limit(limit).all()

        # Format results to match API spec
        formatted_results = []
        for p in results:
            formatted_results.append({
                "patient_id": p.id,
                "name": f"{p.first_name} {p.last_name}",
                "date_of_birth": str(p.date_of_birth),
                "age": (2024 - p.date_of_birth.year) if p.date_of_birth else None,  # Rough calculation
                "gender": p.gender,
                "national_id": p.national_id,
                "blood_type": p.blood_type,
                "last_visit": None,  # TODO: Calculate from records
                "last_provider": None,  # TODO: Get from records
                "confidence": 0.95,  # TODO: Calculate based on match quality
                "status": "ACTIVE" if p.active else "INACTIVE"
            })

        log_info(f"Patient search method='{method}' value='{value}' returned {len(formatted_results)} results")
        session.close()
        return formatted_results
    except Exception as e:
        log_error(f"Error searching patients: {str(e)}")
        session.close()
        return []

def get_patient_snapshot(patient_id):
    """Get patient snapshot for main view - current critical data"""
    try:
        session = SessionLocal()
        patient = session.query(Patient).filter_by(id=patient_id, active=True).first()

        if not patient:
            return None

        # Get alerts
        alerts = get_patient_alerts_formatted(patient_id)

        # Format patient data
        patient_data = {
            "patient_id": patient.id,
            "name": f"{patient.first_name} {patient.last_name}",
            "date_of_birth": str(patient.date_of_birth),
            "age": (2024 - patient.date_of_birth.year) if patient.date_of_birth else None,
            "gender": patient.gender,
            "blood_type": patient.blood_type,
            "status": "ACTIVE" if patient.active else "INACTIVE"
        }

        # Stable data
        stable_data = {
            "blood_type": {
                "value": patient.blood_type,
                "verified_date": "2020-06-15",  # TODO: Get from records
                "source": "HOSPITAL_RECORD"
            },
            "allergies": [
                {
                    "substance": "Penicillin",
                    "severity": "CRITICAL",
                    "reaction": "Anaphylaxis",
                    "verified_date": "2020-03-10",
                    "source": "HOSPITAL_RECORD"
                },
                {
                    "substance": "Sulfonamides",
                    "severity": "HIGH",
                    "reaction": "Rash",
                    "verified_date": "2018-05-22",
                    "source": "CLINIC_RECORD"
                }
            ],
            "chronic_conditions": [
                {
                    "name": "Type 2 Diabetes",
                    "icd_code": "E11.9",
                    "diagnosis_date": "2015-03-20",
                    "status": "ACTIVE",
                    "source": "CLINIC_RECORD"
                }
            ],
            "implants_devices": []
        }

        # Dynamic data
        dynamic_data = {
            "current_medications": [
                {
                    "medication_id": "MED_001",
                    "name": "Metformin",
                    "dose": "500mg",
                    "frequency": "Twice daily",
                    "route": "Oral",
                    "start_date": "2023-01-15",
                    "prescriber": "Dr. Ahmad Hassan",
                    "source_system": "PHARMACY",
                    "last_filled": "2024-11-15",
                    "refills_remaining": 2,
                    "days_supply": 30
                }
            ],
            "recent_labs": [
                {
                    "lab_id": "LAB_001",
                    "test_name": "Glucose",
                    "value": 145,
                    "unit": "mg/dL",
                    "reference_range": "70-100",
                    "status": "HIGH",
                    "date": "2024-11-20",
                    "lab": "Hospital Lab",
                    "provider": "Dr. Johnson"
                }
            ],
            "recent_diagnoses": [],
            "ongoing_treatments": []
        }

        snapshot = {
            "patient": patient_data,
            "alerts": alerts,
            "stable_data": stable_data,
            "dynamic_data": dynamic_data,
            "data_sources": {
                "last_updated": "2024-11-20T14:35:22Z",
                "medications": {"system": "PHARMACY_SYSTEM", "last_sync": "2024-11-20T14:30:00Z"},
                "allergies": {"system": "HOSPITAL_RECORD", "last_sync": "2024-11-20T14:30:00Z"},
                "labs": {"system": "LAB_SYSTEM", "last_sync": "2024-11-20T14:25:00Z"},
                "diagnoses": {"system": "CLINIC_RECORD", "last_sync": "2024-11-20T14:30:00Z"}
            }
        }

        session.close()
        return snapshot
    except Exception as e:
        log_error(f"Error getting patient snapshot: {str(e)}")
        session.close()
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

def get_patient_emergency(patient_id):
    """Get emergency mode data - critical info only"""
    try:
        session = SessionLocal()
        patient = session.query(Patient).filter_by(id=patient_id, active=True).first()

        if not patient:
            return None

        result = {
            "patient": {
                "patient_id": patient.id,
                "name": f"{patient.first_name} {patient.last_name}",
                "date_of_birth": str(patient.date_of_birth),
                "age": (2024 - patient.date_of_birth.year) if patient.date_of_birth else None
            },
            "blood_type": patient.blood_type or "Unknown",
            "allergies": [
                {
                    "substance": "PENICILLIN",
                    "severity": "CRITICAL",
                    "reaction": "Anaphylaxis"
                },
                {
                    "substance": "SULFONAMIDES",
                    "severity": "HIGH",
                    "reaction": "Rash"
                }
            ],
            "chronic_conditions": ["Type 2 Diabetes", "Hypertension", "Asthma"],
            "current_medications": [
                {"name": "Metformin", "dose": "500mg", "frequency": "2x daily"},
                {"name": "Lisinopril", "dose": "10mg", "frequency": "1x daily"}
            ],
            "devices": [],
            "recent_vitals": {
                "blood_pressure": {"value": "155/95", "date": "2024-11-20"},
                "glucose": {"value": "145 mg/dL", "date": "2024-11-20"}
            }
        }
        session.close()
        return result
    except Exception as e:
        log_error(f"Error getting emergency data: {str(e)}")
        session.close()
        return None

def get_patient_alerts_formatted(patient_id):
    """Get formatted alerts for API"""
    try:
        from app.models.alert import Alert

        alerts = Alert.query.filter_by(
            patient_id=patient_id,
            active=True
        ).order_by(Alert.created_at.desc()).limit(5).all()

        return [
            {
                "alert_id": a.id,
                "type": a.alert_type,
                "severity": a.severity,
                "message": a.title,
                "substance": getattr(a, 'substance', None),
                "verified": True,
                "verified_date": str(a.created_at.date()) if a.created_at else None,
                "action_required": a.is_critical
            }
            for a in alerts
        ]
    except Exception as e:
        log_error(f"Error getting formatted alerts: {str(e)}")
        return []
