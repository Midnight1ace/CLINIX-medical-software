"""Structured Logging Utilities"""

import logging
import os
from datetime import datetime

# Configure logging
LOG_DIR = os.path.join(os.path.dirname(__file__), '../../logs')
os.makedirs(LOG_DIR, exist_ok=True)

# Create logger
logger = logging.getLogger('patient_intelligence')
logger.setLevel(logging.INFO)

# File handler
file_handler = logging.FileHandler(os.path.join(LOG_DIR, 'app.log'))
file_handler.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)s - %(name)s - %(message)s'
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def log_info(message):
    """Log info message"""
    logger.info(message)

def log_warning(message):
    """Log warning message"""
    logger.warning(message)

def log_error(message):
    """Log error message"""
    logger.error(message)

def log_debug(message):
    """Log debug message"""
    logger.debug(message)

def log_access(user_id, patient_id, action):
    """Log patient record access"""
    timestamp = datetime.utcnow().isoformat()
    message = f"ACCESS_LOG | User: {user_id} | Patient: {patient_id} | Action: {action} | Time: {timestamp}"
    logger.info(message)
