"""Audit Logging API Routes"""

from flask import Blueprint, request, jsonify
from app.services.audit_service import log_access, get_audit_logs

bp = Blueprint('audit', __name__, url_prefix='/api/audit')

@bp.route('/logs', methods=['GET'])
def get_logs():
    """Get audit logs (admin only)"""
    # TODO: Implement permission check
    
    patient_id = request.args.get('patient_id')
    user_id = request.args.get('user_id')
    
    logs = get_audit_logs(patient_id=patient_id, user_id=user_id)
    
    return jsonify({'logs': logs}), 200

@bp.route('/access-log', methods=['POST'])
def log_patient_access():
    """Log access to patient record"""
    data = request.get_json()
    
    if not data or not data.get('patient_id') or not data.get('user_id'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    log_access(
        patient_id=data['patient_id'],
        user_id=data['user_id'],
        access_type=data.get('access_type', 'view'),
        details=data.get('details')
    )
    
    return jsonify({'message': 'Access logged'}), 201

@bp.route('/export', methods=['POST'])
def export_logs():
    """Export audit logs (admin only)"""
    # TODO: Implement log export
    return jsonify({'message': 'Logs exported'}), 200
