from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from enum import Enum
import secrets
import uvicorn

app = FastAPI(title="AI-Patient-Record-Intelligence API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserRole(str, Enum):
    DOCTOR = "DOCTOR"
    PHARMACIST = "PHARMACIST"
    CLINIC_STAFF = "CLINIC_STAFF"
    ADMIN = "ADMIN"

class SearchMethod(str, Enum):
    PATIENT_ID = "PATIENT_ID"
    NATIONAL_ID = "NATIONAL_ID"
    PARTIAL_NAME = "PARTIAL_NAME"
    QR_CODE = "QR_CODE"
    BARCODE = "BARCODE"
    EMERGENCY = "EMERGENCY"

DEMO_USERS = {
    "dr_johnson": {
        "password": "demo123",
        "role": UserRole.DOCTOR,
        "name": "Dr. Sarah Johnson",
        "user_id": "DR_JOHNSON_001"
    },
    "dr_hassan": {
        "password": "demo123",
        "role": UserRole.DOCTOR,
        "name": "Dr. Ahmad Hassan",
        "user_id": "DR_HASSAN_001"
    },
    "pharm_smith": {
        "password": "demo123",
        "role": UserRole.PHARMACIST,
        "name": "Pharmacist Smith",
        "user_id": "PHARM_SMITH_001"
    }
}

active_sessions = {}

DEMO_PATIENTS = {
    "PAT_987654": {
        "patient_id": "PAT_987654",
        "demographics": {
            "name": "John Smith",
            "date_of_birth": "1960-05-15",
            "age": 64,
            "gender": "M",
            "national_id": "123-45-6789",
            "contact": {
                "phone": "(555) 123-4567",
                "email": "john.smith@email.com",
                "address": "123 Main St, Springfield, IL"
            }
        },
        "stable_data": {
            "blood_type": "O+",
            "allergies": [
                {
                    "substance": "Penicillin",
                    "severity": "CRITICAL",
                    "reaction": "Anaphylaxis risk",
                    "verified_date": "2020-03-10",
                    "source": "Hospital Emergency System"
                },
                {
                    "substance": "Sulfonamides",
                    "severity": "HIGH",
                    "reaction": "Rash",
                    "verified_date": "2020-03-10",
                    "source": "Hospital Emergency System"
                },
                {
                    "substance": "Latex",
                    "severity": "MEDIUM",
                    "reaction": "Contact dermatitis",
                    "verified_date": "2021-07-15",
                    "source": "Clinic Record"
                }
            ],
            "genetic_conditions": [],
            "chronic_conditions": [
                {
                    "condition": "Type 2 Diabetes",
                    "diagnosed_date": "2015-03-20",
                    "status": "ACTIVE",
                    "icd_code": "E11.9"
                },
                {
                    "condition": "Hypertension",
                    "diagnosed_date": "2018-06-10",
                    "status": "ACTIVE",
                    "icd_code": "I10"
                },
                {
                    "condition": "Asthma",
                    "diagnosed_date": "2010-01-15",
                    "status": "CONTROLLED",
                    "icd_code": "J45.909"
                }
            ],
            "implants_devices": [
                {
                    "type": "Pacemaker",
                    "model": "Medtronic Azure XT DR",
                    "date_implanted": "2019-06-22",
                    "location": "Left chest",
                    "serial": "PM-2019-45678"
                }
            ],
            "previous_surgeries": [
                {
                    "surgery": "Pacemaker Implantation",
                    "date": "2019-06-22",
                    "hospital": "Springfield General Hospital",
                    "surgeon": "Dr. Robert Chen"
                },
                {
                    "surgery": "Appendectomy",
                    "date": "1985-09-15",
                    "hospital": "County Hospital",
                    "surgeon": "Dr. Unknown"
                }
            ]
        },
        "dynamic_data": {
            "current_medications": [
                {
                    "name": "Metformin",
                    "generic_name": "Metformin HCl",
                    "dose": "500mg",
                    "frequency": "2x daily (morning, evening)",
                    "route": "Oral",
                    "start_date": "2023-01-15",
                    "prescriber": "Dr. Ahmad Hassan",
                    "indication": "Type 2 Diabetes management",
                    "source_system": "PHARMACY",
                    "last_filled": "2024-11-01",
                    "refills_remaining": 2
                },
                {
                    "name": "Lisinopril",
                    "generic_name": "Lisinopril",
                    "dose": "10mg",
                    "frequency": "1x daily (morning)",
                    "route": "Oral",
                    "start_date": "2023-01-15",
                    "prescriber": "Dr. Ahmad Hassan",
                    "indication": "Hypertension control",
                    "source_system": "PHARMACY",
                    "last_filled": "2024-11-01",
                    "refills_remaining": 3
                },
                {
                    "name": "Albuterol Inhaler",
                    "generic_name": "Albuterol sulfate",
                    "dose": "90mcg",
                    "frequency": "As needed for wheezing",
                    "route": "Inhalation",
                    "start_date": "2020-05-10",
                    "prescriber": "Dr. Sarah Johnson",
                    "indication": "Asthma relief",
                    "source_system": "PHARMACY",
                    "last_filled": "2024-10-15",
                    "refills_remaining": 1
                }
            ],
            "recent_labs": [
                {
                    "test_name": "Blood Glucose (Fasting)",
                    "value": "145 mg/dL",
                    "reference_range": "70-100 mg/dL",
                    "status": "HIGH",
                    "date": "2024-11-20",
                    "ordered_by": "Dr. Sarah Johnson",
                    "facility": "Hospital Lab",
                    "source": "LAB_SYSTEM"
                },
                {
                    "test_name": "HbA1c",
                    "value": "7.2%",
                    "reference_range": "<5.7%",
                    "status": "HIGH",
                    "date": "2024-11-15",
                    "ordered_by": "Dr. Ahmad Hassan",
                    "facility": "Hospital Lab",
                    "source": "LAB_SYSTEM"
                },
                {
                    "test_name": "Blood Pressure",
                    "value": "155/95 mmHg",
                    "reference_range": "<120/80 mmHg",
                    "status": "HIGH",
                    "date": "2024-11-20",
                    "ordered_by": "Dr. Sarah Johnson",
                    "facility": "Emergency Department",
                    "source": "HOSPITAL_SYSTEM"
                },
                {
                    "test_name": "Cholesterol (Total)",
                    "value": "210 mg/dL",
                    "reference_range": "<200 mg/dL",
                    "status": "BORDERLINE_HIGH",
                    "date": "2024-11-15",
                    "ordered_by": "Dr. Ahmad Hassan",
                    "facility": "Hospital Lab",
                    "source": "LAB_SYSTEM"
                }
            ],
            "recent_diagnoses": [
                {
                    "diagnosis": "Hypertension control issue",
                    "icd_code": "I10",
                    "date": "2024-11-20",
                    "provider": "Dr. Sarah Johnson",
                    "facility": "Emergency Department",
                    "status": "ACTIVE",
                    "notes": "Blood pressure elevated, medication adjustment recommended"
                },
                {
                    "diagnosis": "Type 2 Diabetes, uncontrolled",
                    "icd_code": "E11.65",
                    "date": "2024-11-15",
                    "provider": "Dr. Ahmad Hassan",
                    "facility": "Primary Care Clinic",
                    "status": "ACTIVE",
                    "notes": "HbA1c elevated at 7.2%, lifestyle counseling provided"
                }
            ],
            "recent_visits": [
                {
                    "visit_id": "VISIT_2024_1120",
                    "date": "2024-11-20",
                    "type": "Emergency Visit",
                    "facility": "Springfield General Hospital - Emergency Department",
                    "provider": "Dr. Sarah Johnson",
                    "chief_complaint": "Chest pain, shortness of breath",
                    "diagnosis": "Hypertension, angina ruled out",
                    "disposition": "Discharged home with follow-up",
                    "source": "HOSPITAL_SYSTEM"
                },
                {
                    "visit_id": "VISIT_2024_1115",
                    "date": "2024-11-15",
                    "type": "Routine Checkup",
                    "facility": "Primary Care Clinic",
                    "provider": "Dr. Ahmad Hassan",
                    "chief_complaint": "Diabetes follow-up",
                    "diagnosis": "Type 2 Diabetes, Hypertension",
                    "disposition": "Continue current medications, recheck in 3 months",
                    "source": "CLINIC_SYSTEM"
                },
                {
                    "visit_id": "VISIT_2024_1030",
                    "date": "2024-10-30",
                    "type": "Pharmacy Consultation",
                    "facility": "Main Street Pharmacy",
                    "provider": "Pharmacist Smith",
                    "chief_complaint": "Medication refill",
                    "diagnosis": "N/A",
                    "disposition": "Prescriptions refilled",
                    "source": "PHARMACY_SYSTEM"
                }
            ]
        }
    },
    "PAT_654321": {
        "patient_id": "PAT_654321",
        "demographics": {
            "name": "Mary Johnson",
            "date_of_birth": "1955-08-22",
            "age": 69,
            "gender": "F",
            "national_id": "987-65-4321",
            "contact": {
                "phone": "(555) 987-6543",
                "email": "mary.johnson@email.com",
                "address": "456 Oak Ave, Springfield, IL"
            }
        },
        "stable_data": {
            "blood_type": "A-",
            "allergies": [
                {
                    "substance": "Aspirin",
                    "severity": "MEDIUM",
                    "reaction": "GI bleeding",
                    "verified_date": "2019-05-12",
                    "source": "Hospital System"
                }
            ],
            "genetic_conditions": [],
            "chronic_conditions": [
                {
                    "condition": "Osteoarthritis",
                    "diagnosed_date": "2010-03-15",
                    "status": "ACTIVE",
                    "icd_code": "M19.90"
                }
            ],
            "implants_devices": [],
            "previous_surgeries": [
                {
                    "surgery": "Knee Replacement (Right)",
                    "date": "2018-04-10",
                    "hospital": "Springfield General Hospital",
                    "surgeon": "Dr. Michael Torres"
                }
            ]
        },
        "dynamic_data": {
            "current_medications": [
                {
                    "name": "Acetaminophen",
                    "generic_name": "Acetaminophen",
                    "dose": "500mg",
                    "frequency": "3x daily as needed",
                    "route": "Oral",
                    "start_date": "2018-05-01",
                    "prescriber": "Dr. Michael Torres",
                    "indication": "Pain management",
                    "source_system": "PHARMACY",
                    "last_filled": "2024-10-20",
                    "refills_remaining": 5
                }
            ],
            "recent_labs": [],
            "recent_diagnoses": [],
            "recent_visits": []
        }
    }
}

def verify_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format")
    
    token = authorization.replace("Bearer ", "")
    
    if token not in active_sessions:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    session = active_sessions[token]
    if datetime.now() > session["expires_at"]:
        del active_sessions[token]
        raise HTTPException(status_code=401, detail="Token expired")
    
    return session

@app.get("/")
async def root():
    return {"message": "AI-Patient-Record-Intelligence API v1.0", "status": "running"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.post("/api/v1/auth/login")
async def login(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    hospital_id = data.get("hospital_id", "HOSP_001")
    
    if username not in DEMO_USERS:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user = DEMO_USERS[username]
    
    if user["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now() + timedelta(minutes=15)
    
    active_sessions[token] = {
        "user_id": user["user_id"],
        "role": user["role"],
        "name": user["name"],
        "hospital_id": hospital_id,
        "expires_at": expires_at
    }
    
    return {
        "token": token,
        "user_id": user["user_id"],
        "role": user["role"],
        "name": user["name"],
        "hospital_id": hospital_id
    }

@app.post("/api/v1/auth/logout")
async def logout(session: dict = Depends(verify_token), authorization: str = Header(None)):
    token = authorization.replace("Bearer ", "")
    if token in active_sessions:
        del active_sessions[token]
    return {"message": "Logged out successfully"}

@app.get("/api/v1/patients/search")
async def search_patients(
    method: str,
    value: str,
    session: dict = Depends(verify_token)
):
    results = []
    
    if method == "PATIENT_ID":
        if value in DEMO_PATIENTS:
            patient = DEMO_PATIENTS[value]
            results.append({
                "patient_id": patient["patient_id"],
                "name": patient["demographics"]["name"],
                "date_of_birth": patient["demographics"]["date_of_birth"],
                "age": patient["demographics"]["age"],
                "gender": patient["demographics"]["gender"],
                "match_score": 1.0,
                "match_reason": "Exact Patient ID match"
            })
    
    elif method == "PARTIAL_NAME":
        search_term = value.lower()
        for patient_id, patient in DEMO_PATIENTS.items():
            patient_name = patient["demographics"]["name"].lower()
            if search_term in patient_name:
                results.append({
                    "patient_id": patient["patient_id"],
                    "name": patient["demographics"]["name"],
                    "date_of_birth": patient["demographics"]["date_of_birth"],
                    "age": patient["demographics"]["age"],
                    "gender": patient["demographics"]["gender"],
                    "match_score": 0.9 if search_term == patient_name else 0.7,
                    "match_reason": "Name match"
                })
    
    elif method == "NATIONAL_ID":
        for patient_id, patient in DEMO_PATIENTS.items():
            if patient["demographics"]["national_id"] == value:
                results.append({
                    "patient_id": patient["patient_id"],
                    "name": patient["demographics"]["name"],
                    "date_of_birth": patient["demographics"]["date_of_birth"],
                    "age": patient["demographics"]["age"],
                    "gender": patient["demographics"]["gender"],
                    "match_score": 1.0,
                    "match_reason": "Exact National ID match"
                })
    
    results.sort(key=lambda x: x["match_score"], reverse=True)
    
    return {
        "search_method": method,
        "search_value": value,
        "total_results": len(results),
        "results": results
    }

@app.get("/api/v1/patients/{patient_id}/snapshot")
async def get_patient_snapshot(patient_id: str, session: dict = Depends(verify_token)):
    if patient_id not in DEMO_PATIENTS:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    patient = DEMO_PATIENTS[patient_id]
    
    critical_alerts = []
    for allergy in patient["stable_data"]["allergies"]:
        if allergy["severity"] in ["CRITICAL", "HIGH"]:
            critical_alerts.append({
                "type": "ALLERGY",
                "severity": allergy["severity"],
                "message": f"⚠️ {allergy['severity']} ALLERGY: {allergy['substance']} - {allergy['reaction']}"
            })
    
    return {
        "patient_id": patient_id,
        "demographics": patient["demographics"],
        "critical_alerts": critical_alerts,
        "stable_data": patient["stable_data"],
        "dynamic_data": patient["dynamic_data"],
        "last_updated": datetime.now().isoformat(),
        "data_sources": {
            "hospital_system": True,
            "clinic_system": True,
            "pharmacy_system": True,
            "lab_system": True
        }
    }

@app.get("/api/v1/patients/{patient_id}/emergency")
async def get_emergency_data(patient_id: str, session: dict = Depends(verify_token)):
    if patient_id not in DEMO_PATIENTS:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    patient = DEMO_PATIENTS[patient_id]
    
    recent_vitals = [lab for lab in patient["dynamic_data"].get("recent_labs", []) 
                     if lab["test_name"] in ["Blood Pressure", "Blood Glucose (Fasting)", "Heart Rate"]]
    
    return {
        "patient_id": patient_id,
        "patient_name": patient["demographics"]["name"],
        "date_of_birth": patient["demographics"]["date_of_birth"],
        "age": patient["demographics"]["age"],
        "blood_type": patient["stable_data"]["blood_type"],
        "critical_allergies": [
            {
                "substance": allergy["substance"],
                "reaction": allergy["reaction"],
                "severity": allergy["severity"]
            }
            for allergy in patient["stable_data"]["allergies"]
            if allergy["severity"] in ["CRITICAL", "HIGH"]
        ],
        "chronic_conditions": [
            {
                "condition": cond["condition"],
                "status": cond["status"]
            }
            for cond in patient["stable_data"]["chronic_conditions"]
        ],
        "current_medications": [
            {
                "name": med["name"],
                "dose": med["dose"],
                "frequency": med["frequency"]
            }
            for med in patient["dynamic_data"]["current_medications"]
        ],
        "implants_devices": patient["stable_data"]["implants_devices"],
        "recent_vitals": recent_vitals[:3],
        "emergency_mode": True,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v1/patients/{patient_id}/history")
async def get_patient_history(patient_id: str, session: dict = Depends(verify_token)):
    if patient_id not in DEMO_PATIENTS:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    patient = DEMO_PATIENTS[patient_id]
    
    timeline = []
    
    for visit in patient["dynamic_data"].get("recent_visits", []):
        timeline.append({
            "date": visit["date"],
            "type": "VISIT",
            "event_type": visit["type"],
            "provider": visit["provider"],
            "facility": visit["facility"],
            "details": {
                "chief_complaint": visit["chief_complaint"],
                "diagnosis": visit["diagnosis"],
                "disposition": visit["disposition"]
            },
            "source": visit["source"]
        })
    
    for lab in patient["dynamic_data"].get("recent_labs", []):
        timeline.append({
            "date": lab["date"],
            "type": "LAB",
            "event_type": "Laboratory Test",
            "provider": lab["ordered_by"],
            "facility": lab["facility"],
            "details": {
                "test_name": lab["test_name"],
                "value": lab["value"],
                "status": lab["status"]
            },
            "source": lab["source"]
        })
    
    for surgery in patient["stable_data"].get("previous_surgeries", []):
        timeline.append({
            "date": surgery["date"],
            "type": "SURGERY",
            "event_type": "Surgical Procedure",
            "provider": surgery["surgeon"],
            "facility": surgery["hospital"],
            "details": {
                "procedure": surgery["surgery"]
            },
            "source": "HOSPITAL_SYSTEM"
        })
    
    timeline.sort(key=lambda x: x["date"], reverse=True)
    
    return {
        "patient_id": patient_id,
        "patient_name": patient["demographics"]["name"],
        "timeline": timeline,
        "total_events": len(timeline)
    }

@app.get("/api/v1/patients/{patient_id}/ai-summary")
async def get_ai_summary(patient_id: str, session: dict = Depends(verify_token)):
    if patient_id not in DEMO_PATIENTS:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    patient = DEMO_PATIENTS[patient_id]
    
    return {
        "patient_id": patient_id,
        "patient_name": patient["demographics"]["name"],
        "generated_at": datetime.now().isoformat(),
        "disclaimer": "⚠️ AI-generated summary for clinical support only. Always verify against original documents.",
        "summary": {
            "conditions": [
                {
                    "name": cond["condition"],
                    "status": cond["status"],
                    "diagnosed_date": cond["diagnosed_date"],
                    "icd_code": cond["icd_code"],
                    "confidence": "HIGH",
                    "source": "Multiple hospital records"
                }
                for cond in patient["stable_data"]["chronic_conditions"]
            ],
            "medications": [
                {
                    "name": med["name"],
                    "dose": med["dose"],
                    "frequency": med["frequency"],
                    "indication": med["indication"],
                    "prescriber": med["prescriber"],
                    "confidence": "HIGH",
                    "source": f"Pharmacy System (Last filled: {med['last_filled']})"
                }
                for med in patient["dynamic_data"]["current_medications"]
            ],
            "allergies": [
                {
                    "substance": allergy["substance"],
                    "severity": allergy["severity"],
                    "reaction": allergy["reaction"],
                    "confidence": "CRITICAL",
                    "source": f"{allergy['source']} (Verified: {allergy['verified_date']})"
                }
                for allergy in patient["stable_data"]["allergies"]
            ],
            "recent_tests": [
                {
                    "test": lab["test_name"],
                    "value": lab["value"],
                    "date": lab["date"],
                    "status": lab["status"],
                    "confidence": "HIGH",
                    "source": lab["facility"]
                }
                for lab in patient["dynamic_data"].get("recent_labs", [])[:5]
            ],
            "implants_devices": [
                {
                    "type": device["type"],
                    "model": device.get("model", "N/A"),
                    "date_implanted": device["date_implanted"],
                    "confidence": "HIGH",
                    "source": "Hospital surgical records"
                }
                for device in patient["stable_data"]["implants_devices"]
            ]
        },
        "ai_limitations": [
            "Does not diagnose conditions",
            "Does not prescribe medications",
            "Does not make clinical recommendations",
            "Always verify against original source documents"
        ]
    }

@app.get("/api/v1/pharmacy/patients/{patient_id}")
async def get_pharmacy_view(patient_id: str, session: dict = Depends(verify_token)):
    if session["role"] != UserRole.PHARMACIST:
        raise HTTPException(status_code=403, detail="Pharmacist access required")
    
    if patient_id not in DEMO_PATIENTS:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    patient = DEMO_PATIENTS[patient_id]
    
    interaction_warnings = []
    if any(med["name"] == "Lisinopril" for med in patient["dynamic_data"]["current_medications"]):
        if any(med["name"] == "Albuterol Inhaler" for med in patient["dynamic_data"]["current_medications"]):
            interaction_warnings.append({
                "severity": "MINOR",
                "message": "Lisinopril + Albuterol: Monitor for reduced efficacy of Lisinopril",
                "drugs": ["Lisinopril", "Albuterol"]
            })
    
    return {
        "patient_id": patient_id,
        "patient_name": patient["demographics"]["name"],
        "date_of_birth": patient["demographics"]["date_of_birth"],
        "allergies": patient["stable_data"]["allergies"],
        "current_medications": patient["dynamic_data"]["current_medications"],
        "interaction_warnings": interaction_warnings,
        "medication_history": [
            {
                "medication": med["name"],
                "last_filled": med.get("last_filled", "Unknown"),
                "refills_remaining": med.get("refills_remaining", 0),
                "prescriber": med["prescriber"]
            }
            for med in patient["dynamic_data"]["current_medications"]
        ]
    }

if __name__ == "__main__":
    print("=" * 60)
    print("AI-Patient-Record-Intelligence Backend Server")
    print("=" * 60)
    print("\nStarting server on http://localhost:8000")
    print("\nDemo Credentials:")
    print("  Doctor:     dr_johnson / demo123")
    print("  Doctor:     dr_hassan / demo123")
    print("  Pharmacist: pharm_smith / demo123")
    print("\nDemo Patients:")
    print("  PAT_987654 - John Smith (64M)")
    print("  PAT_654321 - Mary Johnson (69F)")
    print("\nAPI Docs: http://localhost:8000/docs")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
