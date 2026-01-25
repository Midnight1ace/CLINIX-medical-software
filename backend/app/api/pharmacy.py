"""Pharmacy Integration API Routes"""

from flask import Blueprint, request, jsonify
from app.services.integration_service import get_pharmacy_records

bp = Blueprint('pharmacy', __name__, url_prefix='/api/pharmacy')

@bp.route('/patient/<patient_id>/medications', methods=['GET'])
def get_medications(patient_id):
    """Get patient medications from pharmacy system"""
    if not patient_id:
        return jsonify({'error': 'Patient ID required'}), 400
    
    medications = get_pharmacy_records(patient_id)
    
    if not medications:
        return jsonify({'error': 'No medication records found'}), 404
    
    return jsonify({'medications': medications}), 200

@bp.route('/patient/<patient_id>/refills', methods=['GET'])
def get_refills(patient_id):
    """Get pending medication refills"""
    if not patient_id:
        return jsonify({'error': 'Patient ID required'}), 400
    
    # TODO: Implement refill retrieval
    return jsonify({'refills': []}), 200

@bp.route('/patient/<patient_id>/interactions', methods=['GET'])
def check_interactions(patient_id):
    """Check for drug interactions"""
    if not patient_id:
        return jsonify({'error': 'Patient ID required'}), 400
    
    # TODO: Implement interaction checking
    return jsonify({'interactions': []}), 200
