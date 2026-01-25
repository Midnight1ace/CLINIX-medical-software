"""Authentication Service"""

from app.models.user import User
from app.utils.security import create_token, verify_token
from app.utils.logging import log_info, log_error
from datetime import datetime
from app.database.connection import db

def authenticate_user(email, password):
    """Authenticate user and return JWT token"""
    try:
        user = User.query.filter_by(email=email).first()
        
        if not user:
            log_error(f"Login attempt with non-existent email: {email}")
            return {'success': False, 'error': 'Invalid credentials'}
        
        if not user.active:
            log_error(f"Login attempt with inactive user: {email}")
            return {'success': False, 'error': 'Account is inactive'}
        
        if not user.check_password(password):
            log_error(f"Failed login attempt for user: {email}")
            return {'success': False, 'error': 'Invalid credentials'}
        
        # Create JWT token
        token = create_token(user.to_dict())
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        log_info(f"User {email} logged in successfully")
        
        return {
            'success': True,
            'token': token,
            'user': user.to_dict()
        }
    except Exception as e:
        log_error(f"Authentication error: {str(e)}")
        return {'success': False, 'error': 'Authentication failed'}

def validate_token(token):
    """Validate JWT token"""
    try:
        payload = verify_token(token)
        if payload:
            return {'valid': True, 'user': payload}
        else:
            return {'valid': False, 'error': 'Invalid token'}
    except Exception as e:
        log_error(f"Token validation error: {str(e)}")
        return {'valid': False, 'error': str(e)}
