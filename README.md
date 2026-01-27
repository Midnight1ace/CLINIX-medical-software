# AI-Patient-Record-Intelligence

**A doctor-first, safety-critical system that turns fragmented patient records into instant, reliable clinical clarity—when every second matters.**

---

## Description

AI-Patient-Record-Intelligence is a hospital clinical information system designed around how doctors actually work. It provides instant access to critical patient data with:

- **Zero Learning Curve**: Intuitive layout with no training needed
- **Safety-First Design**: Critical allergy alerts impossible to miss
- **Emergency Mode**: High-contrast crisis interface for time-critical scenarios
- **Role-Based Access**: Different views for doctors, pharmacists, and clinic staff
- **AI-Powered Summaries**: Structured clinical data with source verification

The system consolidates fragmented patient records from multiple sources (hospital, pharmacy, labs, clinics) into a unified, actionable view that prioritizes life-critical information.

---

## Features

### For Healthcare Providers
- ✅ **Patient Search**: Multiple identification methods (Patient ID, National ID, Name, QR/Barcode)
- ✅ **Patient Snapshot**: Two-panel view separating stable data (blood type, allergies) from dynamic data (medications, labs)
- ✅ **Emergency Mode**: Black background, large text, essential data only
- ✅ **AI Summary**: Structured conditions, medications, allergies with confidence indicators
- ✅ **Role-Based Views**: Customized data emphasis for doctors vs pharmacists
- ✅ **Critical Alerts**: Prominent warning banners for allergies and drug interactions
- ✅ **File Upload**: Drag and drop or browse to upload patient records (PDF, DOC, DOCX, TXT, JPG, PNG)

### Technical Stack
- **Backend**: Python 3.14, aiohttp (async web framework)
- **Frontend**: React 18, Vite, Modern CSS
- **Data**: In-memory demo data (production would use PostgreSQL)
- **Authentication**: Token-based with role detection

---

## Installation & Setup

### Prerequisites

Before you begin, ensure you have:
- **Python 3.9+** (tested with Python 3.14)
- **Node.js 16+** (includes npm)
- **Git** (for cloning the repository)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/CLINIX-medical-software.git
cd CLINIX-medical-software
```

### 2. Backend Setup

```powershell
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install aiohttp aiohttp-cors

# Verify installation
python -c "import aiohttp; print('Backend ready!')"
```

### 3. Frontend Setup

```powershell
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install

# Verify installation
npm list react
```

---

## Running the Application

### Quick Start (Two Terminals Required)

#### Terminal 1: Start Backend Server

```powershell
cd backend
venv\Scripts\python.exe main_aiohttp.py

# macOS/Linux:
# source venv/bin/activate
# python main_aiohttp.py
```

**Expected Output:**
```
============================================================
CLINIX-medical-software Backend Server
============================================================

Starting server on http://localhost:8000

Demo Credentials:
  Doctor:     dr_johnson / demo123
  Pharmacist: pharm_smith / demo123

Demo Patients:
  PAT_987654 - John Smith (64M)
  PAT_654321 - Mary Johnson (69F)
============================================================
```

#### Terminal 2: Start Frontend Server

```powershell
cd frontend
npm run dev
```

**Expected Output:**
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/ (**the 5173 is just an example**)
➜  Network: use --host to expose
```

### 3. Open Browser

Navigate to: **http://localhost:5173**

---

## Usage Guide

### Demo Workflow (3-4 minutes)

#### 1. Login (0:00-0:30)
- **Username:** `dr_johnson`
- **Password:** `demo123`
- Role automatically detected as DOCTOR

#### 2. Patient Search (0:30-1:00)
- Enter Patient ID: `PAT_987654`
- Click **Search**
- Select **John Smith** from results

#### 3. Patient Snapshot View (1:00-2:00)
- **Notice:**
  - Alert banner at top (Penicillin allergy - CRITICAL)
  - Left panel: Stable data (blood type, allergies, chronic conditions)
  - Right panel: Dynamic data (current medications, recent labs)
  - All critical information visible without scrolling

#### 4. Emergency Mode (2:00-2:30)
- Click **🚨 Emergency Mode** button
- Observe:
  - High-contrast black background
  - Large, readable text (48px+)
  - Life-critical data only (blood type, allergies, medications)
  - Fast load time (<1 second)

#### 5. AI Summary (2:30-3:00)
- Return to snapshot view
- Click **AI Summary**
- Review structured data with:
  - Confidence indicators (HIGH, CRITICAL)
  - Source document links
  - Disclaimer about AI limitations

#### 6. Role Switch (3:00-3:30)
- Logout
- Login as **Pharmacist:** `pharm_smith` / `demo123`
- View same patient with medication-focused emphasis

---

## Testing

### API Testing with cURL

```bash
# 1. Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"dr_johnson","password":"demo123","hospital_id":"HOSP_001"}'

# 2. Search Patient (replace TOKEN with token from login)
curl http://localhost:8000/api/v1/patients/search?method=PATIENT_ID&value=PAT_987654 \
  -H "Authorization: Bearer TOKEN"

# 3. Get Patient Snapshot
curl http://localhost:8000/api/v1/patients/PAT_987654/snapshot \
  -H "Authorization: Bearer TOKEN"

# 4. Get Emergency Data
curl http://localhost:8000/api/v1/patients/PAT_987654/emergency \
  -H "Authorization: Bearer TOKEN"
```

### Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2026-01-25T...",
  "version": "1.0.0"
}
```

---

## Demo Data

### Users

| Username     | Password | Role       | Access Level                          |
|--------------|----------|------------|---------------------------------------|
| dr_johnson   | demo123  | DOCTOR     | Full patient data, emergency mode     |
| dr_hassan    | demo123  | DOCTOR     | Full patient data, emergency mode     |
| pharm_smith  | demo123  | PHARMACIST | Medications, allergies, interactions  |

### Patients

**PAT_987654 - John Smith (64M)**
- Blood Type: O+
- Critical Allergies: Penicillin (anaphylaxis risk), Sulfonamides
- Chronic Conditions: Type 2 Diabetes, Hypertension, Asthma
- Implants: Pacemaker (2019)
- Current Medications: Metformin 500mg, Lisinopril 10mg, Albuterol Inhaler
- Recent Labs: Glucose HIGH, HbA1c HIGH, Blood Pressure HIGH

**PAT_654321 - Mary Johnson (69F)**
- Blood Type: A-
- Allergies: Aspirin (GI bleeding)
- Chronic Conditions: Osteoarthritis
- Previous Surgeries: Knee Replacement (2018)
- Current Medications: Acetaminophen 500mg

**PAT_123456 - Robert Davis (58M)**
- Blood Type: B+
- Critical Allergies: None
- Chronic Conditions: Coronary Artery Disease, Hyperlipidemia
- Previous Surgeries: Coronary Bypass (2020)
- Current Medications: Aspirin 81mg, Atorvastatin 40mg, Metoprolol 50mg
- Recent Labs: Troponin HIGH (indicating myocardial infarction), ECG shows ST elevation
- Emergency: Acute Myocardial Infarction (Heart Attack) - Requires immediate intervention

---

## Project Structure

```
AI-Patient-Record-Intelligence/
├───│ 
│   ├── backend/
│   │   ├── venv/                 # Virtual environment
│   │   ├── main_aiohttp.py       # aiohttp server (Python 3.14 compatible)
│   │   ├── requirements.txt      # Python dependencies
│   │   └── .env.example          # Environment variables template
│   │
│   ├── frontend/
│   │   ├── src/
│   │   │   ├── App.jsx           # Main application component
│   │   │   ├── App.css           # Hospital-grade styling
│   │   │   ├── index.css         # Base styles
│   │   │   ├── main.jsx          # React entry point
│   │   │   └── pages/
│   │   │       ├── Login.jsx
│   │   │       ├── PatientSearch.jsx
│   │   │       ├── PatientSnapshot.jsx
│   │   │       ├── EmergencyMode.jsx
│   │   │       └── AISummary.jsx
│   │   ├── index.html            # HTML template
│   │   ├── package.json          # Node dependencies
│   │   └── vite.config.js        # Vite configuration
│   │
│   │
│   ├── QUICKSTART.md             # Quick setup guide
│   └── MANUAL_SETUP.md           # Troubleshooting guide
│
└── README.md                     # Full system architecture
```

---

## Troubleshooting

### Backend Issues

**Error: "Module not found: aiohttp"**
```bash
cd backend
venv\Scripts\activate
pip install aiohttp aiohttp-cors
```

**Error: "Address already in use"**
- Change port in `main_aiohttp.py` (line at bottom: `web.run_app(app, port=8001)`)

### Frontend Issues

**Error: "npm: command not found"**
- Install Node.js from: https://nodejs.org/

**Error: "CORS error in browser console"**
- Ensure backend is running on http://localhost:8000
- Check `vite.config.js` proxy settings

**Error: "Cannot find module 'react'"**
```bash
cd frontend
rm -rf node_modules package-lock.json  # Windows: rmdir /s node_modules, del package-lock.json
npm install
```

### Python 3.14 Compatibility

This project uses **aiohttp** instead of FastAPI to ensure compatibility with Python 3.14. If you encounter issues:
- Verify Python version: `python --version`
- Use `main_aiohttp.py` (not `main.py` or `main_simple.py`)

---

## API Reference

### Authentication

**POST** `/api/v1/auth/login`
```json
Request: {"username": "dr_johnson", "password": "demo123", "hospital_id": "HOSP_001"}
Response: {"token": "...", "user_id": "...", "role": "DOCTOR", "name": "..."}
```

**POST** `/api/v1/auth/logout`
```
Headers: Authorization: Bearer {token}
Response: {"message": "Logged out successfully"}
```

### Patient Operations

**GET** `/api/v1/patients/search?method={METHOD}&value={VALUE}`
- Methods: PATIENT_ID, NATIONAL_ID, PARTIAL_NAME, QR_CODE, BARCODE

**GET** `/api/v1/patients/{patient_id}/snapshot`
- Returns: Full patient data with alerts

**GET** `/api/v1/patients/{patient_id}/emergency`
- Returns: Life-critical data only

**GET** `/api/v1/patients/{patient_id}/history`
- Returns: Timeline of visits, labs, surgeries

**GET** `/api/v1/patients/{patient_id}/ai-summary`
- Returns: AI-structured summary with confidence levels

---

## Security Note

⚠️ **This is a DEMO system only**. Production deployment would require:

- ✅ JWT tokens (not simple token strings)
- ✅ Bcrypt password hashing
- ✅ HTTPS/TLS encryption
- ✅ Database encryption (at rest and in transit)
- ✅ Comprehensive audit logging
- ✅ HIPAA compliance validation
- ✅ Multi-factor authentication
- ✅ Role-based access control (RBAC) with audit trails

**Never use demo credentials in production.**

---

## Credits

### Development Team
- System Architecture & Backend: Axion Team
- Frontend UI/UX: Axion Team
- Clinical Workflow Consulting: Healthcare professionals

### Technologies Used
- **Backend Framework**: [aiohttp](https://docs.aiohttp.org/) - Async HTTP client/server for Python
- **Frontend Framework**: [React](https://react.dev/) - JavaScript library for building user interfaces
- **Build Tool**: [Vite](https://vitejs.dev/) - Next generation frontend tooling
- **CORS Handling**: [aiohttp-cors](https://github.com/aio-libs/aiohttp-cors) - CORS support for aiohttp

### Inspiration
This project was designed with input from healthcare professionals to address real-world clinical workflow challenges in hospitals and clinics.

---

## License

**MIT License**

Copyright (c) 2026 CLINIX-medical-software Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## Contact & Support

For questions, issues, or contributions:
- **Issues**: [GitHub Issues](https://github.com/yourusername/AI-Patient-Record-Intelligence/issues)
- **Documentation**: See `README.md` in project root for full architecture
- **Quick Start**: See `QUICKSTART.md` for abbreviated setup guide

---

## Roadmap

### Current Version (v1.0 - Demo)
- ✅ Basic authentication and role-based access
- ✅ Patient search and snapshot view
- ✅ Emergency mode interface
- ✅ AI summary generation
- ✅ Demo data for 2 patients

### Future Enhancements
- [ ] PostgreSQL database integration
- [ ] Real-time data synchronization
- [ ] Document upload and OCR processing
- [ ] Advanced AI summarization with LLM integration
- [ ] Mobile app (iOS/Android)
- [ ] FHIR API compliance
- [ ] Multi-hospital federation
- [ ] Audit trail and compliance reporting

---

**Version:** 1.0.0  
**Last Updated:** January 25, 2026  
**Status:** Demo Ready ✅
