"""Patient API Routes"""

from flask import Blueprint, request, jsonify
from app.services.patient_service import search_patients, get_patient_snapshot
from app.utils.validation import validate_required_fields

bp = Blueprint('patients', __name__, url_prefix='/api/patients')

@bp.route('/search', methods=['GET'])
def search():
    """Search patients by name, ID, or other criteria"""
    query = request.args.get('q', '').strip()
    
    if not query or len(query) < 2:
        return jsonify({'error': 'Search query must be at least 2 characters'}), 400
    
    results = search_patients(query)
    return jsonify({'patients': results}), 200

@bp.route('/<patient_id>/snapshot', methods=['GET'])
def snapshot(patient_id):
    """Get patient snapshot (main view)"""
    if not patient_id:
        return jsonify({'error': 'Patient ID required'}), 400
    
    snapshot_data = get_patient_snapshot(patient_id)
    
    if not snapshot_data:
        return jsonify({'error': 'Patient not found'}), 404
    
    return jsonify(snapshot_data), 200

@bp.route('/<patient_id>/basic-info', methods=['GET'])
def basic_info(patient_id):
    """Get basic patient information"""
    if not patient_id:
        return jsonify({'error': 'Patient ID required'}), 400
    
    # TODO: Implement basic info retrieval
    return jsonify({'patient_id': patient_id}), 200
