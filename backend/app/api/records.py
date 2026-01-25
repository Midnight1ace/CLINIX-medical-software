"""Medical Records API Routes"""

from flask import Blueprint, request, jsonify
from app.services.patient_service import get_patient_history, get_full_record

bp = Blueprint('records', __name__, url_prefix='/api/records')

@bp.route('/patient/<patient_id>/history', methods=['GET'])
def patient_history(patient_id):
    """Get patient's complete medical history timeline"""
    if not patient_id:
        return jsonify({'error': 'Patient ID required'}), 400
    
    history = get_patient_history(patient_id)
    
    if not history:
        return jsonify({'error': 'Patient not found'}), 404
    
    return jsonify({'history': history}), 200

@bp.route('/patient/<patient_id>/full-record', methods=['GET'])
def full_record(patient_id):
    """Get full patient medical record with all documents"""
    if not patient_id:
        return jsonify({'error': 'Patient ID required'}), 400
    
    record = get_full_record(patient_id)
    
    if not record:
        return jsonify({'error': 'Patient not found'}), 404
    
    return jsonify(record), 200

@bp.route('/document/<document_id>', methods=['GET'])
def get_document(document_id):
    """Get specific medical document"""
    # TODO: Implement document retrieval
    return jsonify({'document_id': document_id}), 200
