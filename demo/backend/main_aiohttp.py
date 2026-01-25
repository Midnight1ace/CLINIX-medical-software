from aiohttp import web
import aiohttp_cors
import secrets
import json
from datetime import datetime, timedelta
from enum import Enum

class UserRole(str, Enum):
    DOCTOR = "DOCTOR"
    PHARMACIST = "PHARMACIST"
    CLINIC_STAFF = "CLINIC_STAFF"
    ADMIN = "ADMIN"

DEMO_USERS = {
    "dr_johnson": {
        "password": "demo123",
        "role": "DOCTOR",
        "name": "Dr. Sarah Johnson",
        "user_id": "DR_JOHNSON_001"
    },
    "dr_hassan": {
        "password": "demo123",
        "role": "DOCTOR",
        "name": "Dr. Ahmad Hassan",
        "user_id": "DR_HASSAN_001"
    },
    "pharm_smith": {
        "password": "demo123",
        "role": "PHARMACIST",
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

def verify_token(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise web.HTTPUnauthorized(text="Missing or invalid authorization")
    
    token = auth_header.replace('Bearer ', '')
    if token not in active_sessions:
        raise web.HTTPUnauthorized(text="Invalid or expired token")
    
    session = active_sessions[token]
    if datetime.now() > session["expires_at"]:
        del active_sessions[token]
        raise web.HTTPUnauthorized(text="Token expired")
    
    return session

async def root(request):
    return web.json_response({"message": "AI-Patient-Record-Intelligence API v1.0", "status": "running"})

async def health_check(request):
    return web.json_response({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

async def login(request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    hospital_id = data.get("hospital_id", "HOSP_001")
    
    if username not in DEMO_USERS or DEMO_USERS[username]["password"] != password:
        raise web.HTTPUnauthorized(text="Invalid credentials")
    
    user = DEMO_USERS[username]
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now() + timedelta(minutes=15)
    
    active_sessions[token] = {
        "user_id": user["user_id"],
        "role": user["role"],
        "name": user["name"],
        "hospital_id": hospital_id,
        "expires_at": expires_at
    }
    
    return web.json_response({
        "token": token,
        "user_id": user["user_id"],
        "role": user["role"],
        "name": user["name"],
        "hospital_id": hospital_id
    })

async def logout(request):
    session = verify_token(request)
    token = request.headers.get('Authorization').replace('Bearer ', '')
    if token in active_sessions:
        del active_sessions[token]
    return web.json_response({"message": "Logged out successfully"})

async def search_patients(request):
    session = verify_token(request)
    method = request.query.get('method')
    value = request.query.get('value')
    
    results = []
    
    if method == "PATIENT_ID" and value in DEMO_PATIENTS:
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
            if search_term in patient["demographics"]["name"].lower():
                results.append({
                    "patient_id": patient["patient_id"],
                    "name": patient["demographics"]["name"],
                    "date_of_birth": patient["demographics"]["date_of_birth"],
                    "age": patient["demographics"]["age"],
                    "gender": patient["demographics"]["gender"],
                    "match_score": 0.9,
                    "match_reason": "Name match"
                })
    
    return web.json_response({
        "search_method": method,
        "search_value": value,
        "total_results": len(results),
        "results": results
    })

async def get_patient_snapshot(request):
    session = verify_token(request)
    patient_id = request.match_info['patient_id']
    
    if patient_id not in DEMO_PATIENTS:
        raise web.HTTPNotFound(text="Patient not found")
    
    patient = DEMO_PATIENTS[patient_id]
    critical_alerts = []
    
    for allergy in patient["stable_data"]["allergies"]:
        if allergy["severity"] in ["CRITICAL", "HIGH"]:
            critical_alerts.append({
                "type": "ALLERGY",
                "severity": allergy["severity"],
                "message": f"⚠️ {allergy['severity']} ALLERGY: {allergy['substance']} - {allergy['reaction']}"
            })
    
    return web.json_response({
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
    })

async def get_emergency_data(request):
    session = verify_token(request)
    patient_id = request.match_info['patient_id']
    
    if patient_id not in DEMO_PATIENTS:
        raise web.HTTPNotFound(text="Patient not found")
    
    patient = DEMO_PATIENTS[patient_id]
    recent_vitals = [lab for lab in patient["dynamic_data"].get("recent_labs", []) 
                     if lab["test_name"] in ["Blood Pressure", "Blood Glucose (Fasting)", "Heart Rate"]]
    
    return web.json_response({
        "patient_id": patient_id,
        "patient_name": patient["demographics"]["name"],
        "date_of_birth": patient["demographics"]["date_of_birth"],
        "age": patient["demographics"]["age"],
        "blood_type": patient["stable_data"]["blood_type"],
        "critical_allergies": [
            {"substance": a["substance"], "reaction": a["reaction"], "severity": a["severity"]}
            for a in patient["stable_data"]["allergies"] if a["severity"] in ["CRITICAL", "HIGH"]
        ],
        "chronic_conditions": [
            {"condition": c["condition"], "status": c["status"]}
            for c in patient["stable_data"]["chronic_conditions"]
        ],
        "current_medications": [
            {"name": m["name"], "dose": m["dose"], "frequency": m["frequency"]}
            for m in patient["dynamic_data"]["current_medications"]
        ],
        "implants_devices": patient["stable_data"]["implants_devices"],
        "recent_vitals": recent_vitals[:3],
        "emergency_mode": True,
        "timestamp": datetime.now().isoformat()
    })

async def get_patient_history(request):
    session = verify_token(request)
    patient_id = request.match_info['patient_id']
    
    if patient_id not in DEMO_PATIENTS:
        raise web.HTTPNotFound(text="Patient not found")
    
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
    
    timeline.sort(key=lambda x: x["date"], reverse=True)
    
    return web.json_response({
        "patient_id": patient_id,
        "patient_name": patient["demographics"]["name"],
        "timeline": timeline,
        "total_events": len(timeline)
    })

async def get_ai_summary(request):
    session = verify_token(request)
    patient_id = request.match_info['patient_id']
    
    if patient_id not in DEMO_PATIENTS:
        raise web.HTTPNotFound(text="Patient not found")
    
    patient = DEMO_PATIENTS[patient_id]
    
    return web.json_response({
        "patient_id": patient_id,
        "patient_name": patient["demographics"]["name"],
        "generated_at": datetime.now().isoformat(),
        "disclaimer": "⚠️ AI-generated summary for clinical support only. Always verify against original documents.",
        "summary": {
            "conditions": [
                {
                    "name": c["condition"],
                    "status": c["status"],
                    "diagnosed_date": c["diagnosed_date"],
                    "icd_code": c["icd_code"],
                    "confidence": "HIGH",
                    "source": "Multiple hospital records"
                }
                for c in patient["stable_data"]["chronic_conditions"]
            ],
            "medications": [
                {
                    "name": m["name"],
                    "dose": m["dose"],
                    "frequency": m["frequency"],
                    "indication": m["indication"],
                    "prescriber": m["prescriber"],
                    "confidence": "HIGH",
                    "source": f"Pharmacy System (Last filled: {m['last_filled']})"
                }
                for m in patient["dynamic_data"]["current_medications"]
            ],
            "allergies": [
                {
                    "substance": a["substance"],
                    "severity": a["severity"],
                    "reaction": a["reaction"],
                    "confidence": "CRITICAL",
                    "source": f"{a['source']} (Verified: {a['verified_date']})"
                }
                for a in patient["stable_data"]["allergies"]
            ],
            "recent_tests": [
                {
                    "test": l["test_name"],
                    "value": l["value"],
                    "date": l["date"],
                    "status": l["status"],
                    "confidence": "HIGH",
                    "source": l["facility"]
                }
                for l in patient["dynamic_data"].get("recent_labs", [])[:5]
            ],
            "implants_devices": [
                {
                    "type": d["type"],
                    "model": d.get("model", "N/A"),
                    "date_implanted": d["date_implanted"],
                    "confidence": "HIGH",
                    "source": "Hospital surgical records"
                }
                for d in patient["stable_data"]["implants_devices"]
            ]
        },
        "ai_limitations": [
            "Does not diagnose conditions",
            "Does not prescribe medications",
            "Does not make clinical recommendations",
            "Always verify against original source documents"
        ]
    })

async def get_pharmacy_view(request):
    session = verify_token(request)
    if session["role"] != "PHARMACIST":
        raise web.HTTPForbidden(text="Pharmacist access required")
    
    patient_id = request.match_info['patient_id']
    if patient_id not in DEMO_PATIENTS:
        raise web.HTTPNotFound(text="Patient not found")
    
    patient = DEMO_PATIENTS[patient_id]
    
    return web.json_response({
        "patient_id": patient_id,
        "patient_name": patient["demographics"]["name"],
        "date_of_birth": patient["demographics"]["date_of_birth"],
        "allergies": patient["stable_data"]["allergies"],
        "current_medications": patient["dynamic_data"]["current_medications"],
        "interaction_warnings": [],
        "medication_history": [
            {
                "medication": m["name"],
                "last_filled": m.get("last_filled", "Unknown"),
                "refills_remaining": m.get("refills_remaining", 0),
                "prescriber": m["prescriber"]
            }
            for m in patient["dynamic_data"]["current_medications"]
        ]
    })

app = web.Application()
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
        allow_methods="*"
    )
})

app.router.add_get('/', root)
app.router.add_get('/health', health_check)
app.router.add_post('/api/v1/auth/login', login)
app.router.add_post('/api/v1/auth/logout', logout)
app.router.add_get('/api/v1/patients/search', search_patients)
app.router.add_get('/api/v1/patients/{patient_id}/snapshot', get_patient_snapshot)
app.router.add_get('/api/v1/patients/{patient_id}/emergency', get_emergency_data)
app.router.add_get('/api/v1/patients/{patient_id}/history', get_patient_history)
app.router.add_get('/api/v1/patients/{patient_id}/ai-summary', get_ai_summary)
app.router.add_get('/api/v1/pharmacy/patients/{patient_id}', get_pharmacy_view)

for route in list(app.router.routes()):
    cors.add(route)

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
    print("\n" + "=" * 60)
    
    web.run_app(app, host='0.0.0.0', port=8000)
