"""AI Summary Generation API Routes"""

from flask import Blueprint, request, jsonify
from app.services.ai_summary_service import generate_summary, generate_emergency_summary

bp = Blueprint('ai_summary', __name__, url_prefix='/api/ai-summary')

@bp.route('/patient/<patient_id>', methods=['GET'])
def get_summary(patient_id):
    """Generate AI summary for patient record"""
    if not patient_id:
        return jsonify({'error': 'Patient ID required'}), 400
    
    summary = generate_summary(patient_id)
    
    if not summary:
        return jsonify({'error': 'Could not generate summary'}), 500
    
    return jsonify({'summary': summary}), 200

@bp.route('/patient/<patient_id>/emergency', methods=['GET'])
def get_emergency_summary(patient_id):
    """Generate emergency mode AI summary (prioritized, concise)"""
    if not patient_id:
        return jsonify({'error': 'Patient ID required'}), 400
    
    summary = generate_emergency_summary(patient_id)
    
    if not summary:
        return jsonify({'error': 'Could not generate emergency summary'}), 500
    
    return jsonify({'summary': summary}), 200

@bp.route('/regenerate', methods=['POST'])
def regenerate_summary():
    """Regenerate AI summary with custom parameters"""
    data = request.get_json()
    patient_id = data.get('patient_id') if data else None
    
    if not patient_id:
        return jsonify({'error': 'Patient ID required'}), 400
    
    # TODO: Implement custom summary generation
    return jsonify({'message': 'Summary regenerated'}), 200
