"""Security Utilities - Encryption, Hashing, JWT"""

import jwt
import os
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    """Hash password for storage"""
    return generate_password_hash(password, method='pbkdf2:sha256')

def verify_password(password, password_hash):
    """Verify password against hash"""
    return check_password_hash(password_hash, password)

def create_token(user_data, expires_in_hours=24):
    """Create JWT token"""
    try:
        payload = {
            'user_id': user_data.get('id'),
            'email': user_data.get('email'),
            'role': user_data.get('role'),
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=expires_in_hours)
        }
        
        secret = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
        token = jwt.encode(payload, secret, algorithm='HS256')
        return token
    except Exception as e:
        print(f"Error creating token: {str(e)}")
        return None

def verify_token(token):
    """Verify JWT token and return payload"""
    try:
        secret = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    except Exception as e:
        print(f"Error verifying token: {str(e)}")
        return None

def encrypt_data(data, key=None):
    """Encrypt sensitive data"""
    # TODO: Implement encryption (e.g., Fernet)
    return data

def decrypt_data(encrypted_data, key=None):
    """Decrypt sensitive data"""
    # TODO: Implement decryption
    return encrypted_data
