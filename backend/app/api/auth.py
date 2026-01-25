"""Authentication API Routes"""

from flask import Blueprint, request, jsonify
from app.services.auth_service import authenticate_user, validate_token
from app.utils.validation import validate_email, validate_password

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and return token"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing credentials'}), 400
    
    # Validate input
    if not validate_email(data['email']):
        return jsonify({'error': 'Invalid email format'}), 400
    
    # Authenticate
    result = authenticate_user(data['email'], data['password'])
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 401

@bp.route('/verify-token', methods=['POST'])
def verify_token():
    """Verify JWT token validity"""
    data = request.get_json()
    token = data.get('token') if data else None
    
    if not token:
        return jsonify({'error': 'Token required'}), 400
    
    result = validate_token(token)
    if result['valid']:
        return jsonify(result), 200
    else:
        return jsonify(result), 401

@bp.route('/logout', methods=['POST'])
def logout():
    """Logout user (token invalidation on frontend)"""
    return jsonify({'message': 'Logged out successfully'}), 200
