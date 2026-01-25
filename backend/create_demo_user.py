#!/usr/bin/env python
"""Create demo user for testing"""

from app import create_app
from app.database.connection import db
from app.models.user import Doctor
from datetime import datetime

app = create_app('development')

with app.app_context():
    # Check if demo user exists
    demo_user = Doctor.query.filter_by(email='demo@hospital.local').first()
    
    if demo_user:
        print(f"Demo user already exists: {demo_user.email}")
    else:
        # Create demo doctor
        demo_doctor = Doctor(
            id='DOC_001',
            email='demo@hospital.local',
            first_name='Demo',
            last_name='Doctor',
            role='doctor',
            active=True,
            license_number='MD123456',
            specialization='General Practice',
            department='Primary Care',
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Set password
        demo_doctor.set_password('demo123')
        
        # Add to database
        db.session.add(demo_doctor)
        db.session.commit()
        
        print(f"Demo user created successfully: {demo_doctor.email}")
        print(f"Password: demo123")
