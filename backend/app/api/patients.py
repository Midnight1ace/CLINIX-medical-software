"""Patient API Routes"""

from fastapi import APIRouter, HTTPException, Query
from app.services.patient_service import search_patients, get_patient_snapshot, get_patient_emergency
from typing import Optional

router = APIRouter()

@router.get("/search")
async def search(
    method: str = Query(..., description="Search method"),
    value: str = Query(..., description="Search value"),
    limit: Optional[int] = Query(10, description="Maximum results")
):
    """Search patients by various methods"""

    if not value or len(value.strip()) < 2:
        raise HTTPException(status_code=400, detail="Search value must be at least 2 characters")

    results = search_patients(method, value.strip(), limit)

    if not results:
        return {"status": "NOT_FOUND", "message": "No patients found"}

    return {
        "status": "FOUND",
        "count": len(results),
        "patients": results
    }

@router.get("/{patient_id}/snapshot")
async def snapshot(patient_id: str):
    """Get patient snapshot (main view)"""

    snapshot_data = get_patient_snapshot(patient_id)

    if not snapshot_data:
        raise HTTPException(status_code=404, detail="Patient not found")

    return snapshot_data

@router.get("/{patient_id}/emergency")
async def emergency(patient_id: str):
    """Get emergency mode data"""

    emergency_data = get_patient_emergency(patient_id)

    if not emergency_data:
        raise HTTPException(status_code=404, detail="Patient not found")

    return emergency_data

@router.get("/{patient_id}/history")
async def history(
    patient_id: str,
    filter: Optional[str] = Query(None, description="Filter by type"),
    sort: Optional[str] = Query("RECENT", description="Sort order"),
    limit: Optional[int] = Query(20, description="Maximum results"),
    offset: Optional[int] = Query(0, description="Offset for pagination")
):
    """Get patient medical history"""

    # TODO: Implement history retrieval
    return {
        "patient_id": patient_id,
        "total_records": 0,
        "events": []
    }

@router.get("/{patient_id}/ai-summary")
async def ai_summary(patient_id: str):
    """Get AI-generated summary"""

    # TODO: Implement AI summary
    return {
        "patient_id": patient_id,
        "generated_at": "2024-11-20T14:45:22Z",
        "disclaimer": "This is an AI-generated summary for clinical support only...",
        "conditions": {"confidence": "HIGH", "items": []},
        "medications": {"confidence": "HIGH", "items": []},
        "allergies": {"confidence": "CRITICAL", "items": []},
        "clinical_notes": "AI summary not yet implemented"
    }
