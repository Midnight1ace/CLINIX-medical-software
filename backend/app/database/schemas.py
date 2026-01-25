"""Database Schemas Definition"""

# This file contains schema definitions for database setup
# Models are defined in app/models/

SCHEMA_VERSION = "1.0.0"

# Patient table schema
PATIENT_SCHEMA = {
    'table': 'patients',
    'columns': [
        'id (VARCHAR)',
        'first_name (VARCHAR)',
        'last_name (VARCHAR)',
        'date_of_birth (DATE)',
        'gender (VARCHAR)',
        'email (VARCHAR, UNIQUE)',
        'phone (VARCHAR)',
        'blood_type (VARCHAR)',
        'allergies (TEXT)',
        'chronic_conditions (TEXT)',
        'created_at (DATETIME)',
        'updated_at (DATETIME)',
        'active (BOOLEAN)'
    ]
}

# Medical record schema
RECORD_SCHEMA = {
    'table': 'medical_records',
    'columns': [
        'id (VARCHAR)',
        'patient_id (VARCHAR, FK)',
        'record_type (VARCHAR)',
        'title (VARCHAR)',
        'description (TEXT)',
        'record_date (DATETIME)',
        'source (VARCHAR)',
        'verified (BOOLEAN)',
        'is_critical (BOOLEAN)',
        'created_at (DATETIME)',
        'updated_at (DATETIME)'
    ]
}

# Alert schema
ALERT_SCHEMA = {
    'table': 'alerts',
    'columns': [
        'id (VARCHAR)',
        'patient_id (VARCHAR, FK)',
        'alert_type (VARCHAR)',
        'severity (VARCHAR)',
        'title (VARCHAR)',
        'description (TEXT)',
        'active (BOOLEAN)',
        'created_at (DATETIME)',
        'resolved_at (DATETIME)',
        'acknowledged_by (VARCHAR)',
        'acknowledged_at (DATETIME)'
    ]
}

# User schema
USER_SCHEMA = {
    'table': 'users',
    'columns': [
        'id (VARCHAR)',
        'email (VARCHAR, UNIQUE)',
        'password_hash (VARCHAR)',
        'first_name (VARCHAR)',
        'last_name (VARCHAR)',
        'role (VARCHAR)',
        'active (BOOLEAN)',
        'last_login (DATETIME)',
        'created_at (DATETIME)',
        'updated_at (DATETIME)'
    ]
}

# Audit log schema
AUDIT_LOG_SCHEMA = {
    'table': 'audit_logs',
    'columns': [
        'id (VARCHAR)',
        'user_id (VARCHAR)',
        'patient_id (VARCHAR)',
        'action (VARCHAR)',
        'details (TEXT)',
        'timestamp (DATETIME)',
        'ip_address (VARCHAR)'
    ]
}
