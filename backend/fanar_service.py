import requests
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Fanar API
FANAR_API_KEY = os.getenv('FANAR_API_KEY', '')
FANAR_BASE_URL = 'https://api.fanar.qa'  # Assuming base URL, adjust if different

def get_patient_data(patient_id):
    """
    Fetch patient data from Fanar API
    """
    if not FANAR_API_KEY:
        return {'error': 'FANAR_API_KEY not configured'}

    try:
        headers = {
            'Authorization': f'Bearer {FANAR_API_KEY}',
            'Content-Type': 'application/json'
        }

        url = f'{FANAR_BASE_URL}/patients/{patient_id}'
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {'error': f'API request failed: {response.status_code}', 'details': response.text}

    except Exception as e:
        return {'error': f'Fanar API error: {str(e)}'}

def search_patients(query):
    """
    Search for patients in Fanar system
    """
    if not FANAR_API_KEY:
        return {'error': 'FANAR_API_KEY not configured'}

    try:
        headers = {
            'Authorization': f'Bearer {FANAR_API_KEY}',
            'Content-Type': 'application/json'
        }

        url = f'{FANAR_BASE_URL}/patients/search'
        params = {'q': query}
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            return {'error': f'API request failed: {response.status_code}', 'details': response.text}

    except Exception as e:
        return {'error': f'Fanar API error: {str(e)}'}

def get_patient_records(patient_id, record_type=None):
    """
    Fetch specific patient records (e.g., medical history, lab results)
    """
    if not FANAR_API_KEY:
        return {'error': 'FANAR_API_KEY not configured'}

    try:
        headers = {
            'Authorization': f'Bearer {FANAR_API_KEY}',
            'Content-Type': 'application/json'
        }

        url = f'{FANAR_BASE_URL}/patients/{patient_id}/records'
        params = {}
        if record_type:
            params['type'] = record_type

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            return {'error': f'API request failed: {response.status_code}', 'details': response.text}

    except Exception as e:
        return {'error': f'Fanar API error: {str(e)}'}