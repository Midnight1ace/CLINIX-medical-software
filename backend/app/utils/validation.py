"""Input Validation Utilities"""

import re
import bleach

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain lowercase letter"
    
    if not re.search(r'[0-9]', password):
        return False, "Password must contain number"
    
    if not re.search(r'[!@#$%^&*]', password):
        return False, "Password must contain special character"
    
    return True, "Valid"

def validate_required_fields(data, required_fields):
    """Validate that required fields are present"""
    missing = []
    for field in required_fields:
        if field not in data or data[field] is None or data[field] == '':
            missing.append(field)
    
    return len(missing) == 0, missing

def sanitize_input(text):
    """Sanitize user input to prevent XSS"""
    return bleach.clean(text, strip=True)

def validate_patient_id(patient_id):
    """Validate patient ID format"""
    return bool(re.match(r'^[a-zA-Z0-9-]+$', patient_id))

def validate_phone(phone):
    """Validate phone number"""
    # Simple validation - adjust pattern as needed
    pattern = r'^\+?1?\d{9,15}$'
    return re.match(pattern, phone.replace('-', '').replace(' ', '')) is not None

def validate_date(date_string, format='%Y-%m-%d'):
    """Validate date format"""
    try:
        from datetime import datetime
        datetime.strptime(date_string, format)
        return True
    except ValueError:
        return False
