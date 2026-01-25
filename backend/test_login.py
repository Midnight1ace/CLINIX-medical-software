#!/usr/bin/env python
"""Test login endpoint"""

import requests
import json

url = "http://localhost:5000/api/auth/login"
data = {
    "email": "demo@hospital.local",
    "password": "demo123"
}

try:
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {str(e)}")
