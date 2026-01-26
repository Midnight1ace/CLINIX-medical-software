import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def generate_ai_summary(patient_data):
    """
    Generate an intelligent clinical summary using Gemini AI
    """
    if not GEMINI_API_KEY:
        return generate_fallback_summary(patient_data)
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        prompt = f"""
You are a medical AI assistant. Generate a comprehensive clinical summary based on the following patient data.

Patient Information:
- Name: {patient_data.get('demographics', {}).get('name', 'Unknown')}
- Age: {patient_data.get('demographics', {}).get('age', 'N/A')}
- Gender: {patient_data.get('demographics', {}).get('gender', 'N/A')}
- Blood Type: {patient_data.get('stable_data', {}).get('blood_type', 'Unknown')}

Allergies:
{json.dumps(patient_data.get('stable_data', {}).get('allergies', []), indent=2)}

Chronic Conditions:
{json.dumps(patient_data.get('stable_data', {}).get('chronic_conditions', []), indent=2)}

Current Medications:
{json.dumps(patient_data.get('dynamic_data', {}).get('current_medications', []), indent=2)}

Recent Diagnoses:
{json.dumps(patient_data.get('dynamic_data', {}).get('recent_diagnoses', []), indent=2)}

Recent Visits:
{json.dumps(patient_data.get('dynamic_data', {}).get('recent_visits', []), indent=2)}

Generate a clinical summary that includes:
1. A brief patient overview with key demographics
2. Critical medical concerns and risk factors
3. Allergy warnings with severity assessment
4. Current treatment plan analysis
5. Care coordination recommendations
6. Potential drug interactions or concerns
7. Suggested follow-up actions

Format the response in clear, professional medical terminology suitable for healthcare providers.
Use markdown formatting for better readability.
"""
        
        response = model.generate_content(prompt)
        return {
            'ai_generated': True,
            'summary_text': response.text,
            'model': 'gemini-2.0-flash-exp'
        }
        
    except Exception as e:
        print(f"Gemini AI error: {e}")
        return generate_fallback_summary(patient_data)


def generate_fallback_summary(patient_data):
    """
    Fallback summary generation without AI
    """
    name = patient_data.get('demographics', {}).get('name', 'Unknown')
    age = patient_data.get('demographics', {}).get('age', 'N/A')
    gender = patient_data.get('demographics', {}).get('gender', 'N/A')
    
    allergies = patient_data.get('stable_data', {}).get('allergies', [])
    conditions = patient_data.get('stable_data', {}).get('chronic_conditions', [])
    medications = patient_data.get('dynamic_data', {}).get('current_medications', [])
    
    summary_parts = []
    summary_parts.append(f"**Patient Overview**\n{name}, {age} year old {gender}")
    
    if allergies:
        allergy_list = ", ".join([f"{a['substance']} ({a['severity']})" for a in allergies])
        summary_parts.append(f"\n\n**⚠️ Allergies**\n{allergy_list}")
    
    if conditions:
        condition_list = ", ".join([c['condition'] for c in conditions])
        summary_parts.append(f"\n\n**Chronic Conditions**\n{condition_list}")
    
    if medications:
        med_list = ", ".join([f"{m['name']} {m['dose']}" for m in medications[:5]])
        summary_parts.append(f"\n\n**Current Medications**\n{med_list}")
    
    summary_parts.append("\n\n*AI summary not available. Please configure GEMINI_API_KEY for enhanced insights.*")
    
    return {
        'ai_generated': False,
        'summary_text': "\n".join(summary_parts),
        'model': 'fallback'
    }


def suggest_data_corrections(field_name, current_value, context):
    """
    Use Gemini to suggest corrections or improvements to patient data
    """
    if not GEMINI_API_KEY:
        return {'suggestions': [], 'confidence': 0}
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        prompt = f"""
You are a medical data quality assistant. Review the following patient data field and suggest corrections if needed.

Field: {field_name}
Current Value: {current_value}
Context: {json.dumps(context, indent=2)}

Analyze:
1. Is the data format correct?
2. Is the value plausible given the context?
3. Are there any obvious errors or inconsistencies?
4. What corrections or improvements would you suggest?

Respond in JSON format:
{{
    "is_valid": true/false,
    "confidence": 0-100,
    "issues": ["list of issues"],
    "suggestions": ["list of suggested corrections"],
    "corrected_value": "suggested correct value if applicable"
}}
"""
        
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        # Clean up markdown code blocks if present
        if '```json' in result_text:
            result_text = result_text.split('```json')[1].split('```')[0].strip()
        elif '```' in result_text:
            result_text = result_text.split('```')[1].split('```')[0].strip()
        
        result = json.loads(result_text)
        return result
        
    except Exception as e:
        print(f"Gemini suggestion error: {e}")
        return {'suggestions': [], 'confidence': 0, 'issues': []}


def analyze_document_with_ai(document_text, filename):
    """
    Use Gemini to extract structured patient data from unstructured medical documents
    """
    if not GEMINI_API_KEY:
        return None
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        prompt = f"""
You are a medical document extraction expert. Extract structured patient information from this medical document.

Document: {filename}

Content:
{document_text[:8000]}

Extract and return ONLY valid JSON (no markdown, no explanation):
{{
    "patient_name": "Full name",
    "age": number,
    "gender": "M/F",
    "date_of_birth": "MM/DD/YYYY or date if found",
    "blood_type": "blood type if found",
    "chief_complaint": "main complaint",
    "diagnoses": ["list of diagnoses from assessment section"],
    "conditions": [
        {{"condition": "name", "status": "ACTIVE", "diagnosed_date": "date or 'See record'"}}
    ],
    "medications": [
        {{"name": "medication", "dose": "dose with unit", "frequency": "frequency"}}
    ],
    "allergies": [
        {{"substance": "allergen", "severity": "HIGH/CRITICAL", "reaction": "reaction description"}}
    ],
    "vital_signs": {{
        "blood_pressure": "value",
        "pulse": "value",
        "temperature": "value"
    }},
    "encounter_date": "date",
    "encounter_type": "type",
    "provider": "Dr. Name",
    "facility": "facility name"
}}

Rules:
- Only include fields where data is clearly found
- Use exact values from the document
- For dates, use consistent format
- For diagnoses, extract from Assessment/Diagnosis section
- For medications, include dose and frequency
"""
        
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        # Clean up markdown code blocks
        if '```json' in result_text:
            result_text = result_text.split('```json')[1].split('```')[0].strip()
        elif '```' in result_text:
            result_text = result_text.split('```')[1].split('```')[0].strip()
        
        result = json.loads(result_text)
        return result
        
    except Exception as e:
        print(f"Gemini document analysis error: {e}")
        return None


def enhance_search_results(query, search_results):
    """
    Use Gemini to rank and enhance search results based on query relevance
    """
    if not GEMINI_API_KEY or not search_results:
        return search_results
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        prompt = f"""
You are a medical search assistant. Rank these patient search results by relevance to the query.

Query: {query}

Search Results:
{json.dumps(search_results, indent=2)}

Return JSON array with ranked results, adding a "relevance_score" (0-100) and "relevance_reason" to each:
[
    {{
        ...original_patient_data,
        "relevance_score": 95,
        "relevance_reason": "Exact name match"
    }}
]

Only return valid JSON, no markdown.
"""
        
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        if '```json' in result_text:
            result_text = result_text.split('```json')[1].split('```')[0].strip()
        elif '```' in result_text:
            result_text = result_text.split('```')[1].split('```')[0].strip()
        
        enhanced_results = json.loads(result_text)
        return enhanced_results
        
    except Exception as e:
        print(f"Gemini search enhancement error: {e}")
        return search_results


def generate_emergency_insights(patient_data):
    """
    Generate critical insights for emergency mode
    """
    if not GEMINI_API_KEY:
        return None
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        prompt = f"""
You are an emergency medicine AI assistant. Analyze this patient data and provide critical insights.

Patient: {patient_data.get('patient_name')}
Age: {patient_data.get('age')}
Allergies: {json.dumps(patient_data.get('critical_allergies', []))}
Conditions: {json.dumps(patient_data.get('chronic_conditions', []))}
Medications: {json.dumps(patient_data.get('current_medications', []))}

Provide:
1. Critical warnings (allergies, drug interactions, contraindications)
2. Risk factors for emergency treatment
3. Important considerations for anesthesia/sedation
4. Recommended precautions

Keep it concise, clear, and actionable. Use markdown formatting.
"""
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        print(f"Gemini emergency insights error: {e}")
        return None


def validate_medication_interactions(medications):
    """
    Check for potential drug interactions
    """
    if not GEMINI_API_KEY or not medications:
        return {'interactions': [], 'warnings': []}
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        med_list = [f"{m['name']} {m['dose']}" for m in medications]
        
        prompt = f"""
You are a clinical pharmacology expert. Analyze these medications for potential interactions.

Medications:
{chr(10).join(med_list)}

Return JSON:
{{
    "interactions": [
        {{
            "medications": ["drug1", "drug2"],
            "severity": "HIGH/MODERATE/LOW",
            "description": "interaction description",
            "recommendation": "what to do"
        }}
    ],
    "warnings": ["list of general warnings"]
}}

Only return valid JSON.
"""
        
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        if '```json' in result_text:
            result_text = result_text.split('```json')[1].split('```')[0].strip()
        elif '```' in result_text:
            result_text = result_text.split('```')[1].split('```')[0].strip()
        
        return json.loads(result_text)
        
    except Exception as e:
        print(f"Gemini medication interaction error: {e}")
        return {'interactions': [], 'warnings': []}
