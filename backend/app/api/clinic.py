"""Clinic Integration API Routes"""

from flask import Blueprint, request, jsonify
from app.services.integration_service import get_clinic_records

bp = Blueprint('clinic', __name__, url_prefix='/api/clinic')

@bp.route('/patient/<patient_id>/appointments', methods=['GET'])
def get_appointments(patient_id):
    """Get patient's clinic appointments"""
    if not patient_id:
        return jsonify({'error': 'Patient ID required'}), 400
    
    appointments = get_clinic_records(patient_id, 'appointments')
    
    if not appointments:
        return jsonify({'error': 'No appointments found'}), 404
    
    return jsonify({'appointments': appointments}), 200

@bp.route('/patient/<patient_id>/visit-history', methods=['GET'])
def get_visit_history(patient_id):
    """Get patient's clinic visit history"""
    if not patient_id:
        return jsonify({'error': 'Patient ID required'}), 400
    
    visits = get_clinic_records(patient_id, 'visits')
    
    if not visits:
        return jsonify({'error': 'No visit history found'}), 404
    
    return jsonify({'visits': visits}), 200

@bp.route('/patient/<patient_id>/vitals', methods=['GET'])
def get_vitals(patient_id):
    """Get patient's latest vital signs"""
    if not patient_id:
        return jsonify({'error': 'Patient ID required'}), 400
    
    # TODO: Implement vitals retrieval
    return jsonify({'vitals': {}}), 200
