from aiohttp import web
import asyncio
import secrets
import json
import os
import re
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path

# noinspection PyUnresolvedReference  
import aiohttp_cors

# Local utilities
from document_processing import extract_document_text
from realtime import EventBus
from storage import InMemoryStorage, PostgresStorage

# Import Gemini AI service
from gemini_service import (
    generate_ai_summary,
    analyze_document_with_ai,
    suggest_data_corrections,
    enhance_search_results,
    generate_emergency_insights,
    validate_medication_interactions
)

# Import Fanar API service
from fanar_service import (
    get_patient_data,
    search_patients as fanar_search_patients,
    get_patient_records
)

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


async def init_app(app):
    db_url = os.getenv("DATABASE_URL", "").strip()
    enable_seed = os.getenv("ENABLE_DB_SEED", "true").lower() in ("1", "true", "yes")

    if db_url:
        storage = PostgresStorage(db_url)
        await storage.connect()
        await storage.init()
        if enable_seed:
            await storage.seed_demo_data(DEMO_PATIENTS)
    else:
        storage = InMemoryStorage(DEMO_PATIENTS)
        await storage.connect()
        await storage.init()
        if enable_seed:
            await storage.seed_demo_data(DEMO_PATIENTS)

    app["storage"] = storage
    app["events"] = EventBus()


async def cleanup_app(app):
    storage = app.get("storage")
    if storage:
        await storage.close()

def verify_token(request, allow_query_token=False):
    auth_header = request.headers.get('Authorization')
    token = None

    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.replace('Bearer ', '')
    elif allow_query_token:
        token = request.query.get('token')

    if not token:
        raise web.HTTPUnauthorized(text="Missing or invalid authorization")

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

async def sync_stream(request):
    session = verify_token(request, allow_query_token=True)
    patient_id_filter = request.query.get("patient_id")
    events = request.app["events"]

    queue = await events.subscribe()

    response = web.StreamResponse(
        status=200,
        headers={
            "Content-Type": "text/event-stream",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )
    await response.prepare(request)

    await response.write(b"event: ready\n")
    await response.write(b"data: {\"status\":\"connected\"}\n\n")

    try:
        while True:
            try:
                event = await asyncio.wait_for(queue.get(), timeout=15)
            except asyncio.TimeoutError:
                await response.write(b": keep-alive\n\n")
                continue

            if patient_id_filter and event.get("patient_id") != patient_id_filter:
                continue

            payload = json.dumps(event, default=str)
            await response.write(f"event: {event.get('type', 'update')}\n".encode("utf-8"))
            await response.write(f"data: {payload}\n\n".encode("utf-8"))
    except (asyncio.CancelledError, ConnectionResetError, BrokenPipeError):
        pass
    finally:
        await events.unsubscribe(queue)

    return response

async def login(request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    hospital_id = data.get("hospital_id", "HOSP_001")
    
    if username not in DEMO_USERS or DEMO_USERS[username]["password"] != password:
        raise web.HTTPUnauthorized(text="Invalid credentials")
    
    user = DEMO_USERS[username]
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now() + timedelta(hours=8)
    
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

    storage = request.app["storage"]
    results = await storage.search_patients(method, value)
    
    return web.json_response({
        "search_method": method,
        "search_value": value,
        "total_results": len(results),
        "results": results
    })

async def search_fanar_patients(request):
    session = verify_token(request)
    query = request.query.get('q', '')

    if not query:
        return web.json_response({"error": "Query parameter 'q' is required"}, status=400)

    fanar_results = fanar_search_patients(query)

    if 'error' in fanar_results:
        return web.json_response(fanar_results, status=500)

    return web.json_response(fanar_results)

async def get_fanar_patient_data(request):
    session = verify_token(request)
    patient_id = request.match_info['patient_id']

    fanar_data = get_patient_data(patient_id)

    if 'error' in fanar_data:
        return web.json_response(fanar_data, status=500)

    return web.json_response(fanar_data)

async def get_fanar_patient_records(request):
    session = verify_token(request)
    patient_id = request.match_info['patient_id']
    record_type = request.query.get('type')

    fanar_records = get_patient_records(patient_id, record_type)

    if 'error' in fanar_records:
        return web.json_response(fanar_records, status=500)

    return web.json_response(fanar_records)

async def get_patient_snapshot(request):
    session = verify_token(request)
    patient_id = request.match_info['patient_id']

    storage = request.app["storage"]
    patient = await storage.get_patient(patient_id)
    if not patient:
        raise web.HTTPNotFound(text="Patient not found")
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

    storage = request.app["storage"]
    patient = await storage.get_patient(patient_id)
    if not patient:
        raise web.HTTPNotFound(text="Patient not found")
    
    # Get all allergies for emergency mode
    all_allergies = [
        {"substance": a["substance"], "reaction": a["reaction"], "severity": a["severity"]}
        for a in patient["stable_data"]["allergies"]
    ]
    
    # Get recent vitals from labs
    recent_vitals = [lab for lab in patient["dynamic_data"].get("recent_labs", []) 
                     if lab["test_name"] in ["Blood Pressure", "Blood Glucose (Fasting)", "Heart Rate"]]
    
    return web.json_response({
        "patient_id": patient_id,
        "patient_name": patient["demographics"]["name"],
        "date_of_birth": patient["demographics"]["date_of_birth"],
        "age": patient["demographics"]["age"],
        "gender": patient["demographics"].get("gender", "Unknown"),
        "blood_type": patient["stable_data"]["blood_type"],
        "critical_allergies": all_allergies,
        "chronic_conditions": [
            {"condition": c["condition"], "status": c["status"]}
            for c in patient["stable_data"]["chronic_conditions"]
        ],
        "current_medications": [
            {"name": m["name"], "dose": m["dose"], "frequency": m["frequency"]}
            for m in patient["dynamic_data"]["current_medications"]
        ],
        "recent_diagnoses": [
            {"diagnosis": d.get("diagnosis"), "date": d.get("date"), "provider": d.get("provider")}
            for d in patient["dynamic_data"].get("recent_diagnoses", [])
        ],
        "recent_visits": [
            {
                "date": v.get("date"),
                "type": v.get("type"),
                "provider": v.get("provider"),
                "facility": v.get("facility"),
                "chief_complaint": v.get("chief_complaint")
            }
            for v in patient["dynamic_data"].get("recent_visits", [])[:3]
        ],
        "implants_devices": patient["stable_data"]["implants_devices"],
        "recent_vitals": recent_vitals[:3],
        "emergency_mode": True,
        "timestamp": datetime.now().isoformat()
    })
    
    # Add AI-generated emergency insights
    emergency_data = response_data
    ai_insights = generate_emergency_insights(emergency_data)
    if ai_insights:
        response_data["ai_insights"] = ai_insights
    
    # Check for medication interactions
    med_warnings = validate_medication_interactions(emergency_data.get('current_medications', []))
    if med_warnings and (med_warnings.get('interactions') or med_warnings.get('warnings')):
        response_data["medication_warnings"] = med_warnings
    
    return web.json_response(response_data)

async def get_patient_history(request):
    session = verify_token(request)
    patient_id = request.match_info['patient_id']

    storage = request.app["storage"]
    patient = await storage.get_patient(patient_id)
    if not patient:
        raise web.HTTPNotFound(text="Patient not found")
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

    storage = request.app["storage"]
    patient = await storage.get_patient(patient_id)
    if not patient:
        raise web.HTTPNotFound(text="Patient not found")

    mode = (request.query.get("mode", "standard") or "standard").lower()
    advanced_mode = mode in ("advanced", "full")

    # Generate AI-powered summary using Gemini
    ai_result = generate_ai_summary(patient)

    interaction_analysis = None
    emergency_insights = None

    if advanced_mode:
        interaction_analysis = validate_medication_interactions(
            patient.get("dynamic_data", {}).get("current_medications", [])
        )
        emergency_insights = generate_emergency_insights({
            "patient_name": patient.get("demographics", {}).get("name", "Unknown"),
            "age": patient.get("demographics", {}).get("age", "Unknown"),
            "critical_allergies": patient.get("stable_data", {}).get("allergies", []),
            "chronic_conditions": patient.get("stable_data", {}).get("chronic_conditions", []),
            "current_medications": patient.get("dynamic_data", {}).get("current_medications", [])
        })

    response = {
        "patient_id": patient_id,
        "patient_name": patient["demographics"]["name"],
        "generated_at": datetime.now().isoformat(),
        "disclaimer": "⚠️ AI-generated summary for clinical support only. Always verify against original documents.",
        "ai_generated_summary": ai_result.get('summary_text', ''),
        "ai_model": ai_result.get('model', 'fallback'),
        "summary": {
            "conditions": [
                {
                    "name": c["condition"],
                    "status": c["status"],
                    "diagnosed_date": c.get("diagnosed_date", "Unknown"),
                    "icd_code": c.get("icd_code", "Pending"),
                    "confidence": "HIGH",
                    "source": c.get("source", "Uploaded document")
                }
                for c in patient["stable_data"]["chronic_conditions"]
            ],
            "medications": [
                {
                    "name": m["name"],
                    "dose": m["dose"],
                    "frequency": m["frequency"],
                    "indication": m.get("indication", "See record"),
                    "prescriber": m.get("prescriber", "Not specified"),
                    "confidence": "HIGH",
                    "source": f"Uploaded document (Last filled: {m.get('last_filled', 'Unknown')})"
                }
                for m in patient["dynamic_data"]["current_medications"]
            ],
            "allergies": [
                {
                    "substance": a["substance"],
                    "severity": a["severity"],
                    "reaction": a["reaction"],
                    "confidence": "CRITICAL",
                    "source": f"{a.get('source', 'Uploaded document')} (Verified: {a.get('verified_date', 'Unknown')})"
                }
                for a in patient["stable_data"]["allergies"]
            ],
            "recent_tests": [
                {
                    "test": l["test_name"],
                    "value": l["value"],
                    "date": l["date"],
                    "status": l.get("status", "Normal"),
                    "confidence": "HIGH",
                    "source": l.get("facility", "Unknown facility")
                }
                for l in patient["dynamic_data"].get("recent_labs", [])[:5]
            ],
            "recent_diagnoses": [
                {
                    "diagnosis": d.get("diagnosis", "Unknown"),
                    "date": d.get("date", "Unknown"),
                    "provider": d.get("provider", "Not specified"),
                    "confidence": "HIGH",
                    "source": "Uploaded document"
                }
                for d in patient["dynamic_data"].get("recent_diagnoses", [])
            ],
            "recent_visits": [
                {
                    "date": v.get("date", "Unknown"),
                    "type": v.get("type", "Medical Encounter"),
                    "provider": v.get("provider", "Not specified"),
                    "facility": v.get("facility", "Unknown"),
                    "chief_complaint": v.get("chief_complaint", "See record"),
                    "diagnosis": v.get("diagnosis", "See record"),
                    "confidence": "HIGH",
                    "source": "Uploaded document"
                }
                for v in patient["dynamic_data"].get("recent_visits", [])
            ],
            "implants_devices": [
                {
                    "type": d["type"],
                    "model": d.get("model", "N/A"),
                    "date_implanted": d.get("date_implanted", "Unknown"),
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
    }

    if advanced_mode:
        response["advanced"] = {
            "interaction_analysis": interaction_analysis,
            "emergency_insights": emergency_insights,
            "mode": "advanced"
        }

    return web.json_response(response)

async def get_pharmacy_view(request):
    session = verify_token(request)
    if session["role"] != "PHARMACIST":
        raise web.HTTPForbidden(text="Pharmacist access required")
    
    patient_id = request.match_info['patient_id']

    storage = request.app["storage"]
    patient = await storage.get_patient(patient_id)
    if not patient:
        raise web.HTTPNotFound(text="Patient not found")

    interaction_analysis = validate_medication_interactions(
        patient.get("dynamic_data", {}).get("current_medications", [])
    )
    
    return web.json_response({
        "patient_id": patient_id,
        "patient_name": patient["demographics"]["name"],
        "date_of_birth": patient["demographics"]["date_of_birth"],
        "allergies": patient["stable_data"]["allergies"],
        "current_medications": patient["dynamic_data"]["current_medications"],
        "interaction_warnings": interaction_analysis.get("warnings", []) if interaction_analysis else [],
        "interaction_analysis": interaction_analysis,
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
async def browse_files(request):
    """List all files in the uploads directory"""
    session = verify_token(request)
    
    uploads_dir = Path("uploads")
    if not uploads_dir.exists():
        uploads_dir.mkdir(parents=True, exist_ok=True)
    
    files = []
    try:
        for file_path in uploads_dir.glob("*"):
            if file_path.is_file():
                stat_info = file_path.stat()
                size_readable = f"{stat_info.st_size / 1024:.2f} KB" if stat_info.st_size < 1024*1024 else f"{stat_info.st_size / (1024*1024):.2f} MB"
                files.append({
                    "name": file_path.name,
                    "path": str(file_path.relative_to(uploads_dir)),
                    "size": stat_info.st_size,
                    "size_readable": size_readable,
                    "modified": datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
                    "type": "document"
                })
    except Exception as e:
        raise web.HTTPInternalServerError(text=f"Error reading files: {str(e)}")
    
    files.sort(key=lambda x: x["modified"], reverse=True)
    
    return web.json_response({
        "total_files": len(files),
        "files": files,
        "upload_directory": str(uploads_dir)
    })

async def get_file_content(request):
    """Get content of a specific file, including full PDF extraction"""
    session = verify_token(request)
    filename = request.match_info['filename']
    
    uploads_dir = Path("uploads")
    file_path = uploads_dir / filename
    
    # Security check: ensure file is within uploads directory
    try:
        if not file_path.resolve().is_relative_to(uploads_dir.resolve()):
            raise web.HTTPForbidden(text="Access denied")
    except ValueError:
        raise web.HTTPForbidden(text="Access denied")
    
    if not file_path.exists():
        raise web.HTTPNotFound(text="File not found")
    
    if not file_path.is_file():
        raise web.HTTPBadRequest(text="Not a file")
    
    try:
        file_bytes = file_path.read_bytes()
        extraction = extract_document_text(filename, file_bytes)
        content = extraction["combined_text"] or extraction["text_content"] or extraction["ocr_text"]
        
        return web.json_response({
            "filename": filename,
            "size": file_path.stat().st_size,
            "content": content,
            "is_pdf": filename.lower().endswith('.pdf'),
            "extraction_method": extraction["extraction_method"],
            "ocr_text": extraction["ocr_text"],
            "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
        })
    except Exception as e:
        raise web.HTTPInternalServerError(text=f"Error reading file: {str(e)}")
async def upload_file(request):
    session = verify_token(request)
    
    try:
        reader = await request.multipart()
        file_content = b''
        filename = ''
        file_mime = ''
        patient_id_override = None
        
        async for field in reader:
            if field.name == 'file':
                filename = field.filename
                file_mime = field.headers.get('Content-Type', '')
                file_content = await field.read()
            elif field.name == 'patient_id':
                patient_id_override = (await field.text()).strip()
        
        if not filename:
            return web.json_response({
                "success": False,
                "message": "Missing file",
                "extracted_data": {}
            }, status=400)
        
        upload_dir = "uploads"
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        file_path = os.path.join(upload_dir, filename)
        with open(file_path, 'wb') as f:
            f.write(file_content)
        
        extraction_result = extract_document_text(filename, file_content)
        combined_text = extraction_result["combined_text"]
        
        extracted_data = extract_patient_data(combined_text, filename)
        extracted_data["raw_text"] = combined_text
        extracted_data["ocr_text"] = extraction_result["ocr_text"]
        extracted_data["extraction_method"] = extraction_result["extraction_method"]
        
        # Try AI-enhanced extraction if available
        ai_extracted = analyze_document_with_ai(combined_text, filename)
        if ai_extracted:
            print(f"✓ AI extraction successful")
            # Merge AI extraction with regex extraction (AI takes precedence)
            for key, value in ai_extracted.items():
                if value and (not extracted_data.get(key) or key in ['diagnoses', 'conditions', 'medications', 'allergies']):
                    extracted_data[key] = value
        
        print(f"=== EXTRACTED DATA ===")
        print(f"Date: {extracted_data.get('encounter_date')}")
        print(f"Provider: {extracted_data.get('provider')}")
        print(f"Type: {extracted_data.get('encounter_type')}")
        print(f"Facility: {extracted_data.get('facility')}")
        
        storage = request.app["storage"]
        events = request.app["events"]

        if patient_id_override and patient_id_override != "NEW_PATIENT":
            extracted_data["patient_id"] = patient_id_override
            if extracted_data.get("patient_record"):
                extracted_data["patient_record"]["patient_id"] = patient_id_override

        if extracted_data.get('patient_id') and extracted_data.get('patient_record'):
            patient_id = extracted_data['patient_id']
            existing_patient = await storage.get_patient(patient_id)
            patient_record = extracted_data['patient_record']

            if existing_patient and patient_id_override:
                patient_record = merge_patient_records(existing_patient, patient_record)

            await storage.upsert_patient(patient_id, patient_record)
            print(f"✓ Patient record created/updated: {patient_id} - {extracted_data.get('patient_name')}")

            await events.publish({
                "type": "patient_updated",
                "patient_id": patient_id,
                "source": "document_upload",
                "timestamp": datetime.now().isoformat()
            })

        await storage.add_document({
            "patient_id": extracted_data.get("patient_id"),
            "filename": filename,
            "mime_type": file_mime,
            "storage_path": file_path,
            "size_bytes": len(file_content),
            "extracted_data": extracted_data,
            "ocr_text": extraction_result["ocr_text"]
        })

        await events.publish({
            "type": "document_uploaded",
            "patient_id": extracted_data.get("patient_id"),
            "filename": filename,
            "timestamp": datetime.now().isoformat()
        })
        
        return web.json_response({
            "success": True,
            "message": f"File '{filename}' processed successfully",
            "filename": filename,
            "file_size": len(file_content),
            "upload_timestamp": datetime.now().isoformat(),
            "extracted_data": extracted_data,
            "patient_id": extracted_data.get('patient_id'),
            "patient_name": extracted_data.get('patient_name'),
            "patient_created": bool(extracted_data.get('patient_id'))
        })
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return web.json_response({
            "success": False,
            "message": f"Upload failed: {str(e)}",
            "extracted_data": {}
        }, status=500)

def merge_patient_records(existing_record, new_record):
    merged = json.loads(json.dumps(existing_record))

    merged.setdefault("stable_data", {})
    merged.setdefault("dynamic_data", {})

    def merge_list(target_list, source_list, key):
        existing_keys = {item.get(key) for item in target_list if item.get(key)}
        for item in source_list:
            item_key = item.get(key)
            if item_key and item_key in existing_keys:
                continue
            target_list.append(item)
            if item_key:
                existing_keys.add(item_key)

    # Stable data merges
    stable = merged["stable_data"]
    stable.setdefault("allergies", [])
    stable.setdefault("chronic_conditions", [])
    stable.setdefault("implants_devices", [])
    stable.setdefault("previous_surgeries", [])

    merge_list(stable["allergies"], new_record.get("stable_data", {}).get("allergies", []), "substance")
    merge_list(stable["chronic_conditions"], new_record.get("stable_data", {}).get("chronic_conditions", []), "condition")
    merge_list(stable["implants_devices"], new_record.get("stable_data", {}).get("implants_devices", []), "type")
    merge_list(stable["previous_surgeries"], new_record.get("stable_data", {}).get("previous_surgeries", []), "surgery")

    # Dynamic data merges
    dynamic = merged["dynamic_data"]
    dynamic.setdefault("current_medications", [])
    dynamic.setdefault("recent_labs", [])
    dynamic.setdefault("recent_diagnoses", [])
    dynamic.setdefault("recent_visits", [])

    merge_list(dynamic["current_medications"], new_record.get("dynamic_data", {}).get("current_medications", []), "name")
    merge_list(dynamic["recent_labs"], new_record.get("dynamic_data", {}).get("recent_labs", []), "test_name")
    merge_list(dynamic["recent_diagnoses"], new_record.get("dynamic_data", {}).get("recent_diagnoses", []), "diagnosis")
    merge_list(dynamic["recent_visits"], new_record.get("dynamic_data", {}).get("recent_visits", []), "visit_id")

    return merged

def extract_patient_data(text_content, filename):
    extracted = {
        "patient_id": None,
        "patient_name": None,
        "date_of_birth": None,
        "age": None,
        "gender": None,
        "blood_type": None,
        "allergies": [],
        "medications": [],
        "conditions": [],
        "vital_signs": {},
        "chief_complaint": None,
        "diagnoses": [],
        "encounter_date": None,
        "encounter_type": None,
        "provider": None,
        "facility": None,
        "raw_text": text_content if text_content else "",
        "patient_record": None
    }
    
    if not text_content or len(text_content.strip()) < 10:
        return extracted
    
    name_patterns = [
        r'Patient Name[:\s]+([A-Za-z]+,\s*[A-Za-z]+)',
        r'Patient Name[:\s]+([A-Za-z\s]+?)(?:\n|Date)',
        r'Name[:\s]+([A-Za-z\s,]+?)(?:\n|$)'
    ]
    for pattern in name_patterns:
        match = re.search(pattern, text_content, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            # Clean up name - remove extra text
            name = re.sub(r'\s+', ' ', name)
            if len(name) > 2 and len(name) < 50:
                extracted['patient_name'] = name
                break
    
    # Extract age - be more specific
    age_patterns = [
        r'(\d{1,3})\s*y/?o\s+(?:WF|WM|BF|BM|male|female)',
        r'(\d{1,3})\s*(?:year|years)\s*old',
        r'\(Age:\s*(\d{1,3})\)',
        r'Age:\s*(\d{1,3})'
    ]
    for pattern in age_patterns:
        age_match = re.search(pattern, text_content, re.IGNORECASE)
        if age_match:
            age = int(age_match.group(1))
            if 0 < age < 120:
                extracted['age'] = age
                break
    
    # Extract gender - be more specific
    gender_patterns = [
        (r'(\d{1,3})\s*y/?o\s+(WF|WM|BF|BM)', 2),
        (r'Gender[:\s]+(Male|Female|M|F)', 1),
        (r'\b(male|female)\s+(?:who|patient)', 1),
        (r'(Mr|Ms|Mrs)\.', 1)
    ]
    for pattern, group_idx in gender_patterns:
        gender_match = re.search(pattern, text_content, re.IGNORECASE)
        if gender_match:
            g = gender_match.group(group_idx).upper()
            if 'F' in g or 'FEMALE' in g.upper() or 'MS' in g or 'MRS' in g:
                extracted['gender'] = 'F'
                break
            elif 'M' in g or 'MALE' in g.upper() or g == 'MR':
                extracted['gender'] = 'M'
                break
    
    # Extract DOB with multiple patterns
    dob_patterns = [
        r'(?:DOB|Date of Birth|Birth Date)[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'(?:DOB|Date of Birth)[:\s]+([A-Za-z]+\s+\d{1,2},\s+\d{4})'
    ]
    for pattern in dob_patterns:
        dob_match = re.search(pattern, text_content, re.IGNORECASE)
        if dob_match:
            extracted['date_of_birth'] = dob_match.group(1)
            break
    
    blood_match = re.search(r'\b(A|B|AB|O)[+-]\b', text_content)
    if blood_match:
        extracted['blood_type'] = blood_match.group(0)
    
    # Extract allergies - multiple patterns
    allergy_patterns = [
        r'Allerg(?:y|ies)[:\s]+(.*?)(?:\n\n|\nSocial History|\nMedications|\n[A-Z][a-z]+ History|$)',
        r'Allergy[:\s]+([^\n]+)'
    ]
    
    for pattern in allergy_patterns:
        allergy_section = re.search(pattern, text_content, re.IGNORECASE | re.DOTALL)
        if allergy_section:
            allergy_text = allergy_section.group(1).strip()
            
            # Check for "No known allergies"
            if re.search(r'no\s+known\s+allerg|none|nka|nkda', allergy_text, re.IGNORECASE):
                break
            
            # Look for specific allergen names
            common_allergens = ['Penicillin', 'Sulfa', 'Sulfonamides', 'Aspirin', 'Ibuprofen', 'Latex', 'Codeine', 'Morphine', 'Peanut', 'Shellfish']
            for allergen in common_allergens:
                if re.search(allergen, allergy_text, re.IGNORECASE):
                    severity = "HIGH"
                    if re.search(r'anaphyla|severe|critical', allergy_text, re.IGNORECASE):
                        severity = "CRITICAL"
                    
                    # Try to extract reaction
                    reaction = "See medical record"
                    reaction_match = re.search(rf'{allergen}[:\s;]+(.*?)(?:\.|;|\n|$)', allergy_text, re.IGNORECASE)
                    if reaction_match:
                        reaction_text = reaction_match.group(1).strip()
                        if len(reaction_text) > 5 and len(reaction_text) < 100:
                            reaction = reaction_text
                    
                    extracted['allergies'].append({
                        "substance": allergen,
                        "severity": severity,
                        "reaction": reaction,
                        "verified_date": datetime.now().strftime("%Y-%m-%d"),
                        "source": f"Uploaded document: {filename}"
                    })
            break
    
    med_patterns = [
        r'(?:Medication|Medications|Current Medications|Rx)[:\s]+(.*?)(?:\n\n|\n[A-Z]|$)',
        r'(?:taking|prescribed)[:\s]+(.*?)(?:\.|$)'
    ]
    for pattern in med_patterns:
        med_section = re.search(pattern, text_content, re.IGNORECASE | re.DOTALL)
        if med_section:
            med_text = med_section.group(1)
            common_meds = ['Metformin', 'Lisinopril', 'Atorvastatin', 'Omeprazole', 'Amlodipine', 'Metoprolol', 'Aspirin', 'Ibuprofen', 'Acetaminophen', 'Tylenol', 'Advil']
            for med in common_meds:
                if re.search(med, med_text, re.IGNORECASE):
                    dose_match = re.search(rf'{med}\s*(\d+\s*mg)', med_text, re.IGNORECASE)
                    extracted['medications'].append({
                        "name": med,
                        "dose": dose_match.group(1) if dose_match else "See record",
                        "frequency": "As prescribed",
                        "source": f"Uploaded document: {filename}"
                    })
            break
    
    condition_patterns = [
        r'(?:Past Medical History|Medical History|PMH)[:\s]+(.*?)(?:\n\n|\nSocial History|\nAllerg|\nMedication|$)',
        r'(?:History of Present Illness|HPI)[:\s]+(.*?)(?:\n\n|\nPast Medical|$)',
        r'(?:Diagnosis|Assessment|Impression)[:\s]+(.*?)(?:\n\n|\nPlan|$)'
    ]
    conditions_found = []
    common_conditions = ['Diabetes', 'Hypertension', 'HTN', 'Asthma', 'COPD', 'CHF', 'Heart Failure', 'Angina', 'Chest Pain', 'CAD', 'Coronary', 'Peptic Ulcer']
    
    for pattern in condition_patterns:
        section = re.search(pattern, text_content, re.IGNORECASE | re.DOTALL)
        if section:
            section_text = section.group(1)
            for condition in common_conditions:
                if re.search(rf'\b{condition}\b', section_text, re.IGNORECASE) and condition not in conditions_found:
                    conditions_found.append(condition)
                    
                    # Try to extract date if available
                    date_pattern = rf'{condition}.*?(\d{{1,2}}[/-]\d{{1,2}}[/-]\d{{2,4}}|\d{{4}})'
                    date_match = re.search(date_pattern, section_text, re.IGNORECASE)
                    diagnosed_date = date_match.group(1) if date_match else "See record"
                    
                    extracted['conditions'].append({
                        "condition": condition,
                        "status": "ACTIVE",
                        "diagnosed_date": diagnosed_date,
                        "source": f"Uploaded document: {filename}"
                    })
    
    bp_match = re.search(r'(?:BP|Blood Pressure)[:\s]*(\d{2,3}[/]\d{2,3})', text_content, re.IGNORECASE)
    if bp_match:
        extracted['vital_signs']['blood_pressure'] = bp_match.group(1)
    
    pulse_match = re.search(r'(?:Pulse|HR|Heart Rate)[:\s]*(\d{2,3})', text_content, re.IGNORECASE)
    if pulse_match:
        extracted['vital_signs']['pulse'] = pulse_match.group(1)
    
    temp_match = re.search(r'(?:Temp|Temperature)[:\s]*(\d{2,3}(?:\.\d)?)', text_content, re.IGNORECASE)
    if temp_match:
        extracted['vital_signs']['temperature'] = temp_match.group(1)
    
    chief_complaint_match = re.search(r'(?:Chief Complaint|CC)[:\s]+(.*?)(?:\n\n|\n[A-Z][a-z]+:|$)', text_content, re.IGNORECASE | re.DOTALL)
    if chief_complaint_match:
        extracted['chief_complaint'] = chief_complaint_match.group(1).strip()
    
    diagnosis_patterns = [
        r'(?:Assessment|Diagnosis|Diagnoses)[:\s]+(.*?)(?:\n\n|\n[A-Z][a-z]+:|$)',
        r'(?:Impression)[:\s]+(.*?)(?:\n\n|\n[A-Z][a-z]+:|$)'
    ]
    for pattern in diagnosis_patterns:
        diag_match = re.search(pattern, text_content, re.IGNORECASE | re.DOTALL)
        if diag_match:
            diag_text = diag_match.group(1).strip()
            diag_lines = [line.strip() for line in diag_text.split('\n') if line.strip() and len(line.strip()) > 3]
            for line in diag_lines[:5]:
                line_clean = re.sub(r'^[-\d.)\s]+', '', line).strip()
                if line_clean:
                    extracted['diagnoses'].append(line_clean)
            break
    
    encounter_date_patterns = [
        r'Date of (?:Examination|Visit|Encounter|Service)[:\s]+([A-Za-z]+\s+\d{1,2},\s+\d{4})',
        r'Date of (?:Examination|Visit|Encounter|Service)[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'(?:Encounter|Visit|Service) Date[:\s]+([A-Za-z]+\s+\d{1,2},\s+\d{4})',
        r'(?:Encounter|Visit|Service) Date[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'^Date[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'Date[:\s]+([A-Za-z]+\s+\d{1,2},\s+\d{4})'
    ]
    for pattern in encounter_date_patterns:
        date_match = re.search(pattern, text_content, re.IGNORECASE | re.MULTILINE)
        if date_match:
            extracted['encounter_date'] = date_match.group(1).strip()
            break
    
    encounter_type_patterns = [
        r'(?:History and Physical|H&P)',
        r'(?:Progress Note)',
        r'(?:Discharge Summary)',
        r'(?:Consultation)',
        r'(?:Emergency|ED|ER)',
        r'(?:Operative Report)',
        r'(?:Office Visit)',
        r'(?:Follow[- ]up)'
    ]
    for pattern in encounter_type_patterns:
        if re.search(pattern, text_content, re.IGNORECASE):
            type_match = re.search(pattern, text_content, re.IGNORECASE)
            if type_match:
                extracted['encounter_type'] = type_match.group(0)
                break
    
    if not extracted['encounter_type']:
        if re.search(r'emergency|urgent|acute', text_content, re.IGNORECASE):
            extracted['encounter_type'] = 'Emergency Department Visit'
        elif re.search(r'admission|admit|hospital', text_content, re.IGNORECASE):
            extracted['encounter_type'] = 'Inpatient Admission'
        else:
            extracted['encounter_type'] = 'Medical Encounter'
    
    provider_patterns = [
        r'Attending (?:Physician|Doctor|Provider)[:\s]+Dr\.\s+([A-Z][a-z]+\s+[A-Z][a-z]+)',
        r'(?:Physician|Doctor|Provider)[:\s]+Dr\.\s+([A-Z][a-z]+\s+[A-Z][a-z]+)',
        r'(?:Seen by|Examined by)[:\s]+Dr\.\s+([A-Z][a-z]+\s+[A-Z][a-z]+)',
        r'Dr\.\s+([A-Z][a-z]+\s+[A-Z][a-z]+)'
    ]
    for pattern in provider_patterns:
        provider_match = re.search(pattern, text_content)
        if provider_match:
            provider_name = provider_match.group(1).strip()
            if len(provider_name) > 3 and not provider_name.startswith('Ms') and not provider_name.startswith('Mr'):
                extracted['provider'] = 'Dr. ' + provider_name
                break
    
    if not extracted['provider']:
        source_match = re.search(r'Referral Source[:\s]+([A-Za-z\s]+?)(?:\n|$)', text_content, re.IGNORECASE)
        if source_match:
            source = source_match.group(1).strip()
            if source and source != 'Patient' and len(source) < 50:
                extracted['facility'] = source
    
    facility_patterns = [
        r'(?:Facility|Hospital|Clinic|Medical Center)[:\s]+([A-Z][A-Za-z\s]+(?:Hospital|Clinic|Medical Center|Health|Healthcare))',
        r'([A-Z][A-Za-z\s]+(?:Hospital|Clinic|Medical Center|Health|Healthcare))',
        r'(?:at|from)\s+([A-Z][A-Za-z\s]+(?:Hospital|Clinic|Medical Center|Health|Healthcare))'
    ]
    for pattern in facility_patterns:
        facility_match = re.search(pattern, text_content)
        if facility_match:
            facility_name = facility_match.group(1).strip()
            if len(facility_name) > 5 and len(facility_name) < 100:
                extracted['facility'] = facility_name
                break
    
    if not extracted['facility'] and re.search(r'emergency|ER|ED', text_content, re.IGNORECASE):
        extracted['facility'] = 'Emergency Department'
    
    if extracted['patient_name']:
        patient_id = f"PAT_{secrets.token_hex(3).upper()}"
        extracted['patient_id'] = patient_id
        
        # Build recent visit from encounter data
        recent_visit = {
            "visit_id": f"VIS_{secrets.token_hex(3).upper()}",
            "date": extracted.get('encounter_date') or datetime.now().strftime("%Y-%m-%d"),
            "type": extracted.get('encounter_type') or "Medical Encounter",
            "provider": extracted.get('provider') or "Not specified",
            "facility": extracted.get('facility') or "Not specified",
            "chief_complaint": extracted.get('chief_complaint') or "See record",
            "diagnosis": ", ".join(extracted.get('diagnoses', [])) if extracted.get('diagnoses') else "See record",
            "notes": f"Uploaded from document: {filename}"
        }
        
        extracted['patient_record'] = {
            "patient_id": patient_id,
            "demographics": {
                "name": extracted['patient_name'],
                "date_of_birth": extracted['date_of_birth'] or "Unknown",
                "age": extracted['age'] or 0,
                "gender": extracted['gender'] or "Unknown",
                "national_id": "Pending",
                "contact": {
                    "phone": "Pending",
                    "email": "Pending",
                    "address": "Pending"
                }
            },
            "stable_data": {
                "blood_type": extracted['blood_type'] or "Unknown",
                "allergies": extracted['allergies'],
                "genetic_conditions": [],
                "chronic_conditions": [
                    {
                        "condition": c['condition'],
                        "diagnosed_date": c['diagnosed_date'],
                        "status": c['status'],
                        "icd_code": "Pending"
                    } for c in extracted['conditions']
                ],
                "implants_devices": []
            },
            "dynamic_data": {
                "current_medications": [
                    {
                        "name": m['name'],
                        "generic_name": m['name'],
                        "dose": m['dose'],
                        "frequency": m['frequency'],
                        "route": "Oral",
                        "start_date": datetime.now().strftime("%Y-%m-%d"),
                        "prescriber": extracted.get('provider') or "See record",
                        "indication": "See record",
                        "source_system": "UPLOAD",
                        "last_filled": datetime.now().strftime("%Y-%m-%d"),
                        "refills_remaining": 0
                    } for m in extracted['medications']
                ],
                "recent_labs": [],
                "recent_diagnoses": [
                    {
                        "diagnosis": diag,
                        "date": extracted.get('encounter_date') or datetime.now().strftime("%Y-%m-%d"),
                        "provider": extracted.get('provider') or "Not specified",
                        "icd_code": "Pending"
                    } for diag in extracted.get('diagnoses', [])
                ],
                "recent_visits": [recent_visit]
            }
        }
    
    return extracted

app = web.Application()
app.on_startup.append(init_app)
app.on_cleanup.append(cleanup_app)
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
app.router.add_get('/api/v1/sync/stream', sync_stream)
app.router.add_post('/api/v1/auth/login', login)
app.router.add_post('/api/v1/auth/logout', logout)
app.router.add_get('/api/v1/patients/search', search_patients)
app.router.add_get('/api/v1/fanar/patients/search', search_fanar_patients)
app.router.add_get('/api/v1/fanar/patients/{patient_id}', get_fanar_patient_data)
app.router.add_get('/api/v1/fanar/patients/{patient_id}/records', get_fanar_patient_records)
app.router.add_post('/api/v1/patients/upload', upload_file)
app.router.add_get('/api/v1/patients/{patient_id}/snapshot', get_patient_snapshot)
app.router.add_get('/api/v1/patients/{patient_id}/emergency', get_emergency_data)
app.router.add_get('/api/v1/patients/{patient_id}/history', get_patient_history)
app.router.add_get('/api/v1/patients/{patient_id}/ai-summary', get_ai_summary)
app.router.add_get('/api/v1/pharmacy/patients/{patient_id}', get_pharmacy_view)
app.router.add_get('/api/v1/files/browse', browse_files)
app.router.add_get('/api/v1/files/{filename}', get_file_content)

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
