"""
AI-Patient-Record-Intelligence - FastAPI Backend Demo
Doctor-first, safety-critical patient record system
"""

from fastapi import FastAPI, HTTPException, Depends, status, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import json
from pathlib import Path

# MODELS

class User(BaseModel):
    user_id: str
    username: str
    name: str
    role: str  # DOCTOR, PHARMACIST, CLINIC_STAFF
    hospital_id: str

class LoginRequest(BaseModel):
    username: str
    password: str
    hospital_id: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    name: str
    role: str
    expires_in: int

class Patient(BaseModel):
    patient_id: str
    name: str
    date_of_birth: str
    age: int
    gender: str
    blood_type: str
    status: str

class Allergy(BaseModel):
    substance: str
    severity: str  # CRITICAL, HIGH, MEDIUM
    reaction: str
    verified_date: str

class Medication(BaseModel):
    name: str
    dose: str
    frequency: str
    start_date: str
    source_system: str

class LabResult(BaseModel):
    test_name: str
    value: float
    unit: str
    status: str
    date: str

class Alert(BaseModel):
    alert_id: str
    type: str
    severity: str
    message: str
    action_required: bool

class PatientSnapshot(BaseModel):
    patient: Patient
    alerts: List[Alert]
    stable_data: Dict[str, Any]
    dynamic_data: Dict[str, Any]
    data_sources: Dict[str, Any]

class PatientEmergency(BaseModel):
    patient: Patient
    blood_type: str
    allergies: List[Allergy]
    chronic_conditions: List[str]
    current_medications: List[Medication]
    devices: List[Dict[str, Any]]

class HistoryEvent(BaseModel):
    event_id: str
    date: str
    type: str
    facility: str
    provider: str
    description: str
    status: str

class AISummary(BaseModel):
    patient_id: str
    generated_at: str
    conditions: Dict[str, Any]
    medications: Dict[str, Any]
    allergies: Dict[str, Any]
    clinical_notes: str

# DEMO DATA

DEMO_USERS = {
    "dr_johnson": {
        "user_id": "DR_JOHNSON_001",
        "username": "dr_johnson",
        "password": "demo123",  # In production: hashed
        "name": "Dr. Sarah Johnson",
        "role": "DOCTOR",
        "hospital_id": "HOSP_001"
    },
    "dr_hassan": {
        "user_id": "DR_HASSAN_001",
        "username": "dr_hassan",
        "password": "demo123",
        "name": "Dr. Ahmad Hassan",
        "role": "DOCTOR",
        "hospital_id": "HOSP_001"
    },
    "pharm_smith": {
        "user_id": "PHARM_SMITH_001",
        "username": "pharm_smith",
        "password": "demo123",
        "name": "Maria Smith",
        "role": "PHARMACIST",
        "hospital_id": "HOSP_001"
    }
}

DEMO_PATIENTS = {
    "PAT_987654": {
        "patient_id": "PAT_987654",
        "name": "John Smith",
        "date_of_birth": "1960-05-15",
        "age": 64,
        "gender": "M",
        "blood_type": "O+",
        "status": "ACTIVE",
        "national_id": "123-45-6789"
    },
    "PAT_654321": {
        "patient_id": "PAT_654321",
        "name": "Mary Johnson",
        "date_of_birth": "1955-08-22",
        "age": 69,
        "gender": "F",
        "blood_type": "A-",
        "status": "ACTIVE",
        "national_id": "987-65-4321"
    }
}

# APP INITIALIZATION

app = FastAPI(
    title="AI-Patient-Record-Intelligence Demo",
    description="Doctor-first, safety-critical patient record system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory token storage (for demo only)
active_tokens = {}

# AUTHENTICATION ENDPOINTS

@app.post("/api/v1/auth/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    Login with username and password.
    Demo credentials: dr_johnson / demo123
    """
    user = DEMO_USERS.get(request.username)
    
    if not user or user["password"] != request.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Create demo token (normally would use JWT)
    token = f"token_{user['user_id']}_{datetime.now().timestamp()}"
    active_tokens[token] = {
        "user_id": user["user_id"],
        "role": user["role"],
        "expires_at": datetime.now() + timedelta(minutes=15)
    }
    
    return LoginResponse(
        access_token=token,
        token_type="Bearer",
        user_id=user["user_id"],
        name=user["name"],
        role=user["role"],
        expires_in=900
    )

@app.post("/api/v1/auth/logout")
async def logout(authorization: str = Header(None)):
    """Logout and invalidate token."""
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:]
        if token in active_tokens:
            del active_tokens[token]
    
    return {"message": "Successfully logged out"}

# PATIENT SEARCH ENDPOINTS

@app.get("/api/v1/patients/search")
async def search_patient(
    method: str,
    value: str,
    authorization: str = Header(None)
):
    """
    Search patient by multiple methods:
    - PATIENT_ID: PAT_987654
    - PARTIAL_NAME: John Smith
    - NATIONAL_ID: 123-45-6789
    """
    if not authorization or "Bearer " not in authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    results = []
    
    if method == "PATIENT_ID":
        if value in DEMO_PATIENTS:
            results.append(DEMO_PATIENTS[value])
    
    elif method == "PARTIAL_NAME":
        for patient in DEMO_PATIENTS.values():
            if value.lower() in patient["name"].lower():
                results.append(patient)
    
    elif method == "NATIONAL_ID":
        for patient in DEMO_PATIENTS.values():
            if patient.get("national_id") == value:
                results.append(patient)
    
    if not results:
        return {
            "status": "NOT_FOUND",
            "message": "No patients found"
        }
    
    return {
        "status": "FOUND",
        "count": len(results),
        "patients": results
    }

# PATIENT SNAPSHOT ENDPOINT

@app.get("/api/v1/patients/{patient_id}/snapshot", response_model=PatientSnapshot)
async def get_patient_snapshot(patient_id: str, authorization: str = Header(None)):
    """
    Get complete patient snapshot - the main clinical view.
    All critical data visible without scrolling.
    """
    if not authorization or "Bearer " not in authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    if patient_id not in DEMO_PATIENTS:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    patient_data = DEMO_PATIENTS[patient_id]
    
    # Build alerts based on patient data
    alerts = []
    if patient_id == "PAT_987654":
        alerts = [
            Alert(
                alert_id="ALR_001",
                type="ALLERGY_ALERT",
                severity="CRITICAL",
                message="Penicillin allergy detected - Anaphylaxis risk",
                action_required=True
            ),
            Alert(
                alert_id="ALR_002",
                type="DRUG_INTERACTION",
                severity="HIGH",
                message="Possible interaction: Aspirin + Warfarin",
                action_required=False
            )
        ]
    
    # Stable data (locked, rarely changes)
    stable_data = {
        "blood_type": {
            "value": patient_data["blood_type"],
            "verified_date": "2020-06-15",
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
                "status": "ACTIVE"
            },
            {
                "name": "Hypertension",
                "icd_code": "I10",
                "diagnosis_date": "2010-01-15",
                "status": "ACTIVE"
            }
        ],
        "implants_devices": [
            {
                "type": "Pacemaker",
                "manufacturer": "Medtronic",
                "implant_date": "2019-06-22",
                "location": "Left chest"
            }
        ]
    }
    
    # Dynamic data (timestamped, changes frequently)
    dynamic_data = {
        "current_medications": [
            {
                "name": "Metformin",
                "dose": "500mg",
                "frequency": "Twice daily",
                "start_date": "2023-01-15",
                "prescriber": "Dr. Ahmad Hassan",
                "source_system": "PHARMACY",
                "last_filled": "2024-11-15",
                "refills_remaining": 2
            },
            {
                "name": "Lisinopril",
                "dose": "10mg",
                "frequency": "Once daily",
                "start_date": "2024-11-20",
                "prescriber": "Dr. Sarah Johnson",
                "source_system": "CLINIC",
                "last_filled": "2024-11-20",
                "refills_remaining": 0
            }
        ],
        "recent_labs": [
            {
                "test_name": "Glucose",
                "value": 145,
                "unit": "mg/dL",
                "reference_range": "70-100",
                "status": "HIGH",
                "date": "2024-11-20"
            },
            {
                "test_name": "HbA1c",
                "value": 7.2,
                "unit": "%",
                "reference_range": "<5.7",
                "status": "HIGH",
                "date": "2024-11-15"
            }
        ],
        "recent_diagnoses": [
            {
                "name": "Hypertension, uncontrolled",
                "icd_code": "I10",
                "date": "2024-11-20",
                "provider": "Dr. Sarah Johnson"
            }
        ]
    }
    
    return PatientSnapshot(
        patient=Patient(**patient_data),
        alerts=alerts,
        stable_data=stable_data,
        dynamic_data=dynamic_data,
        data_sources={
            "last_updated": datetime.now().isoformat(),
            "medications": {"system": "PHARMACY_SYSTEM", "last_sync": "2024-11-20T14:30:00Z"},
            "allergies": {"system": "HOSPITAL_RECORD", "last_sync": "2024-11-20T14:30:00Z"},
            "labs": {"system": "LAB_SYSTEM", "last_sync": "2024-11-20T14:25:00Z"}
        }
    )

# EMERGENCY MODE ENDPOINT

@app.get("/api/v1/patients/{patient_id}/emergency", response_model=PatientEmergency)
async def get_patient_emergency(patient_id: str, authorization: str = Header(None)):
    """
    Emergency mode: simplified critical data only.
    Loads in <1 second. High contrast. No scroll.
    """
    if not authorization or "Bearer " not in authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    if patient_id not in DEMO_PATIENTS:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    patient_data = DEMO_PATIENTS[patient_id]
    
    return PatientEmergency(
        patient=Patient(**patient_data),
        blood_type="O+ Rh+",
        allergies=[
            Allergy(
                substance="PENICILLIN",
                severity="CRITICAL",
                reaction="Anaphylaxis",
                verified_date="2020-03-10"
            ),
            Allergy(
                substance="SULFONAMIDES",
                severity="HIGH",
                reaction="Rash",
                verified_date="2018-05-22"
            ),
            Allergy(
                substance="LATEX",
                severity="MEDIUM",
                reaction="Contact dermatitis",
                verified_date="2015-01-10"
            )
        ],
        chronic_conditions=[
            "Type 2 Diabetes",
            "Hypertension",
            "Asthma"
        ],
        current_medications=[
            Medication(
                name="Metformin",
                dose="500mg",
                frequency="2x daily",
                start_date="2023-01-15",
                source_system="PHARMACY"
            ),
            Medication(
                name="Lisinopril",
                dose="10mg",
                frequency="1x daily",
                start_date="2024-11-20",
                source_system="CLINIC"
            )
        ],
        devices=[
            {
                "type": "PACEMAKER",
                "notes": "Do not use defibrillator. Contact cardiology.",
                "implant_date": "2019-06-22"
            }
        ]
    )

# HISTORY ENDPOINT

@app.get("/api/v1/patients/{patient_id}/history")
async def get_patient_history(patient_id: str, authorization: str = Header(None)):
    """Get full medical history - timeline view."""
    if not authorization or "Bearer " not in authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    if patient_id not in DEMO_PATIENTS:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return {
        "patient_id": patient_id,
        "total_records": 5,
        "events": [
            {
                "event_id": "EVT_20241120_001",
                "date": "2024-11-20T08:30:00Z",
                "type": "EMERGENCY_VISIT",
                "facility": "Main Hospital ER",
                "provider": "Dr. Sarah Johnson",
                "description": "Chest pain assessment and ECG",
                "status": "DISCHARGED",
                "ai_summary_available": True
            },
            {
                "event_id": "EVT_20241115_001",
                "date": "2024-11-15T10:00:00Z",
                "type": "CLINIC_VISIT",
                "facility": "Primary Care Clinic",
                "provider": "Dr. Ahmad Hassan",
                "description": "Diabetes and hypertension checkup",
                "status": "COMPLETED",
                "ai_summary_available": True
            },
            {
                "event_id": "EVT_20241110_001",
                "date": "2024-11-10T14:00:00Z",
                "type": "LAB_WORK",
                "facility": "Hospital Lab",
                "provider": "Lab Tech",
                "description": "Blood Panel: Glucose, HbA1c, Lipid Panel",
                "status": "COMPLETED",
                "ai_summary_available": False
            }
        ]
    }

# AI SUMMARY ENDPOINT

@app.get("/api/v1/patients/{patient_id}/ai-summary")
async def get_ai_summary(patient_id: str, authorization: str = Header(None)):
    """
    Get AI-generated clinical summary.
    AI structures data but NEVER diagnoses, prescribes, or recommends.
    """
    if not authorization or "Bearer " not in authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    if patient_id not in DEMO_PATIENTS:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return {
        "patient_id": patient_id,
        "generated_at": datetime.now().isoformat(),
        "disclaimer": "This is an AI-generated summary for clinical support only. Always verify against original documents. AI cannot diagnose, prescribe, or make treatment decisions.",
        "conditions": {
            "confidence": "HIGH",
            "items": [
                {
                    "name": "Type 2 Diabetes",
                    "status": "ACTIVE_MANAGEMENT",
                    "since": "2015-03-20",
                    "sources": [
                        {
                            "document_id": "DOC_002",
                            "document_name": "Clinic Visit Note",
                            "date": "2024-11-15",
                            "excerpt": "Type 2 diabetes well controlled with metformin..."
                        }
                    ]
                },
                {
                    "name": "Hypertension",
                    "status": "ACTIVE_MANAGEMENT",
                    "since": "2010-01-15",
                    "sources": [
                        {
                            "document_id": "DOC_001",
                            "document_name": "Hospital Record",
                            "date": "2024-11-20",
                            "excerpt": "Hypertension management ongoing..."
                        }
                    ]
                }
            ]
        },
        "medications": {
            "confidence": "HIGH",
            "items": [
                {
                    "name": "Metformin",
                    "dose": "500mg",
                    "frequency": "Twice daily",
                    "since": "2023-01-15",
                    "sources": [{"document_id": "DOC_003", "document_name": "Pharmacy Record"}]
                },
                {
                    "name": "Lisinopril",
                    "dose": "10mg",
                    "frequency": "Once daily",
                    "since": "2024-11-20",
                    "sources": [{"document_id": "DOC_001", "document_name": "Clinic Record"}]
                }
            ]
        },
        "allergies": {
            "confidence": "CRITICAL",
            "items": [
                {
                    "substance": "Penicillin",
                    "reaction": "Anaphylaxis",
                    "severity": "CRITICAL",
                    "verified": True
                },
                {
                    "substance": "Sulfonamides",
                    "reaction": "Rash",
                    "severity": "HIGH",
                    "verified": True
                }
            ]
        },
        "clinical_notes": "AI noticed consistent diabetes management across all sources. No contradictions detected. Allergy information verified across multiple records."
    }

# PHARMACIST INTEGRATION ENDPOINT

@app.get("/api/v1/pharmacy/patients/{patient_id}")
async def get_pharmacist_view(patient_id: str, authorization: str = Header(None)):
    """
    Pharmacist-specific view: Same patient data, different emphasis.
    Emphasizes medications, allergies, and drug interactions.
    """
    if not authorization or "Bearer " not in authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    if patient_id not in DEMO_PATIENTS:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    patient_data = DEMO_PATIENTS[patient_id]
    
    return {
        "patient": patient_data,
        "role": "PHARMACIST",
        "medication_interactions": [
            {
                "drugs": ["Metformin", "Lisinopril"],
                "interaction": "Compatible",
                "status": "OK"
            },
            {
                "drugs": ["Metformin", "Aspirin"],
                "interaction": "Monitor Glucose",
                "status": "CAUTION"
            }
        ],
        "medication_history": [
            {
                "name": "Metformin 500mg",
                "status": "Current",
                "prescriber": "Dr. Hassan",
                "last_filled": "2024-11-15",
                "refills_remaining": 2
            },
            {
                "name": "Lisinopril 10mg",
                "status": "Current",
                "prescriber": "Dr. Johnson",
                "last_filled": "2024-11-20",
                "refills_remaining": 0
            },
            {
                "name": "Atorvastatin 20mg",
                "status": "Discontinued",
                "discontinued_date": "2024-09-15"
            }
        ],
        "critical_allergies": [
            "Penicillin (Anaphylaxis)",
            "Sulfonamides (Rash)",
            "Latex (Contact Dermatitis)"
        ]
    }

# HEALTH CHECK

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "AI-Patient-Record-Intelligence Demo API"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
