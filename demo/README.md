# AI-Patient-Record-Intelligence DEMO

A working demonstration of the doctor-first, safety-critical patient record system.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+ (backend)
- Node.js 16+ (frontend)
- npm or yarn

### 1. Backend Setup (Terminal 1)

```bash
cd demo/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
python main.py
```

**Backend runs on:** `http://localhost:8000`

### 2. Frontend Setup (Terminal 2)

```bash
cd demo/frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

**Frontend runs on:** `http://localhost:5173`

### 3. Open Browser

Go to: **http://localhost:5173**

---

## 🔐 Demo Credentials

### Doctors
- **Username:** `dr_johnson`
- **Password:** `demo123`
- **Role:** DOCTOR

Alternative:
- **Username:** `dr_hassan`
- **Password:** `demo123`

### Pharmacist
- **Username:** `pharm_smith`
- **Password:** `demo123`
- **Role:** PHARMACIST

---

## 🧪 Demo Patient Data

### Patient 1: John Smith (Main Demo)
- **Patient ID:** `PAT_987654`
- **Age:** 64 | DOB: 1960-05-15
- **Blood Type:** O+
- **Allergies:** Penicillin (CRITICAL), Sulfonamides, Latex
- **Chronic Conditions:** Type 2 Diabetes, Hypertension, Asthma
- **Implants:** Pacemaker (2019)
- **Current Meds:** Metformin 500mg, Lisinopril 10mg

### Patient 2: Mary Johnson
- **Patient ID:** `PAT_654321`
- **Age:** 69 | DOB: 1955-08-22
- **Blood Type:** A-

---

## 📋 Demo Workflow

### 1. Login (0:00-0:30)
```
→ Use: dr_johnson / demo123
→ Observe: Role automatically detected (DOCTOR)
```

### 2. Patient Search (0:30-1:00)
```
→ Search for: PAT_987654
→ Results: John Smith (perfect match)
→ Click: SELECT PATIENT
```

### 3. Patient Snapshot (1:00-2:00)
```
→ Observe: ALL critical data visible (no scroll)
→ Notice: Alert banner at top (Penicillin allergy)
→ Left side: Stable data (locked, blood type, allergies)
→ Right side: Dynamic data (medications, labs, timestamped)
```

### 4. Key Features to Highlight
```
→ Stable vs Dynamic Data distinction
→ Alert banner (impossible to miss)
→ Original data sources shown
→ Patient header with key info
```

### 5. Emergency Mode (2:00-2:30)
```
→ Click: [🚨 Emergency Mode]
→ Observe: Black background, large text, high contrast
→ Data shows: Blood type, allergies, chronic conditions, meds
→ Fast load: < 1 second
```

### 6. AI Summary (2:30-3:00)
```
→ Go back to snapshot
→ Look for: AI Summary option
→ See: Structured data with source links
→ Notice: Disclaimer about AI limitations
```

### 7. Role Switch (3:00-3:30)
```
→ Logout
→ Login as: pharm_smith / demo123
→ View same patient: Different emphasis (medications focus)
→ Show: Drug interactions, medication history
```

---

## 🔌 API Endpoints

### Authentication
```
POST /api/v1/auth/login
POST /api/v1/auth/logout
```

### Patient Search
```
GET /api/v1/patients/search?method=PATIENT_ID&value=PAT_987654
GET /api/v1/patients/search?method=PARTIAL_NAME&value=John%20Smith
```

### Patient Data
```
GET /api/v1/patients/{patient_id}/snapshot
GET /api/v1/patients/{patient_id}/emergency
GET /api/v1/patients/{patient_id}/history
GET /api/v1/patients/{patient_id}/ai-summary
```

### Pharmacy
```
GET /api/v1/pharmacy/patients/{patient_id}
```

### Health Check
```
GET /health
```

---

## 🧪 Test API with cURL

### 1. Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "dr_johnson",
    "password": "demo123",
    "hospital_id": "HOSP_001"
  }'
```

### 2. Search Patient
```bash
TOKEN="your_token_here"
curl http://localhost:8000/api/v1/patients/search?method=PATIENT_ID&value=PAT_987654 \
  -H "Authorization: Bearer $TOKEN"
```

### 3. Get Snapshot
```bash
curl http://localhost:8000/api/v1/patients/PAT_987654/snapshot \
  -H "Authorization: Bearer $TOKEN"
```

### 4. Get Emergency Data
```bash
curl http://localhost:8000/api/v1/patients/PAT_987654/emergency \
  -H "Authorization: Bearer $TOKEN"
```

### 5. Get AI Summary
```bash
curl http://localhost:8000/api/v1/patients/PAT_987654/ai-summary \
  -H "Authorization: Bearer $TOKEN"
```

---

## 📁 Project Structure

```
demo/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example           # Environment variables
│   └── __pycache__/           # Python cache
│
└── frontend/
    ├── src/
    │   ├── main.jsx           # React entry point
    │   ├── App.jsx            # Main app component
    │   ├── App.css            # Main styles
    │   ├── index.css          # Base styles
    │   ├── pages/
    │   │   ├── Login.jsx      # Login page
    │   │   ├── PatientSearch.jsx
    │   │   ├── PatientSnapshot.jsx
    │   │   ├── EmergencyMode.jsx
    │   │   └── AISummary.jsx
    │   └── components/        # (optional)
    ├── index.html             # HTML template
    ├── package.json           # Node dependencies
    ├── vite.config.js         # Vite configuration
    └── node_modules/          # Installed packages
```

---

## 🎨 UI Features Implemented

### ✅ Login Screen
- Hospital credential entry
- Demo credentials displayed
- Error handling

### ✅ Patient Search
- Multiple search methods (Patient ID, Name, National ID)
- Results ranking
- Patient selection

### ✅ Patient Snapshot (Main View)
- Two-column layout (Stable vs Dynamic data)
- Alert banner with critical warnings
- Patient header with key demographics
- Color-coded data (green = normal, yellow = warning, red = critical)
- Timestamped information
- Source system indicators

### ✅ Emergency Mode
- High contrast (black background)
- Large readable text (48px+)
- Essential data only
- One-button exit
- Fast load time

### ✅ AI Summary
- Structured conditions, medications, allergies
- Source document links
- Confidence indicators
- Disclaimer about AI limitations

### ✅ Role-Based Views
- Different emphasis for different roles
- Same backend, different UI

---

## 🔒 Security in Demo

⚠️ **Note:** This is a **demo only**. Production would include:

✅ JWT tokens (not demo tokens)
✅ Bcrypt password hashing
✅ HTTPS/TLS encryption
✅ Comprehensive audit logging
✅ Database encryption
✅ HIPAA compliance validation

---

## 🐛 Troubleshooting

### Backend won't start
```
Error: Address already in use
→ Solution: Change port in main.py (default 8000)
```

### Frontend can't connect to API
```
Error: CORS error in browser console
→ Solution: Check backend is running on http://localhost:8000
→ Solution: Verify vite.config.js proxy settings
```

### npm dependencies error
```
→ Solution: Delete node_modules and package-lock.json
→ Solution: Run: npm install again
```

### Python dependencies error
```
→ Solution: Ensure Python 3.9+
→ Solution: Run: pip install --upgrade pip
→ Solution: Run: pip install -r requirements.txt
```

---

## 📊 Demo Data Structure

### Patient Snapshot Contains:
- ✅ Patient demographics
- ✅ Alert banner (critical warnings)
- ✅ Stable data (blood type, allergies, chronic conditions)
- ✅ Dynamic data (medications, labs, diagnoses)
- ✅ Data sources (which system provided each piece of data)
- ✅ Last update timestamps

### Emergency Mode Contains:
- ✅ Blood type (large, prominent)
- ✅ Critical allergies
- ✅ Chronic conditions
- ✅ Current medications
- ✅ Implanted devices
- ✅ Recent vitals

### AI Summary Contains:
- ✅ Structured conditions
- ✅ Medications with sources
- ✅ Allergies (critical/verified)
- ✅ Recent tests
- ✅ Clinical notes (no diagnosis/prescription)
- ✅ Disclaimer about AI limitations

---

## 🎯 Key Demo Points

### What Judges Should Notice:

1. **Zero Learning Curve**
   - No training needed
   - Intuitive layout
   - Clear data hierarchy

2. **Doctor-First Design**
   - Critical data visible immediately
   - No unnecessary clicks
   - Realistic hospital workflow

3. **Safety First**
   - Alert banner impossible to miss
   - Emergency mode for crisis
   - Original data always accessible

4. **Real-World Integration**
   - Multiple patient ID methods
   - Multi-system data merging
   - Role-based views

5. **AI That Knows Its Limits**
   - Structures data only
   - Never diagnoses
   - Always links to sources

---

## 📝 Notes

- Demo uses in-memory data (no database)
- Tokens expire after 15 minutes
- All demo data is synthetic
- API responses mimic real hospital systems

---

## 🚀 Next Steps

### To Deploy:
1. See [DEPLOYMENT.md](../DEPLOYMENT.md) for production setup
2. Configure PostgreSQL database
3. Set up HTTPS/SSL certificates
4. Configure CORS for production domain
5. Implement JWT security
6. Add comprehensive logging

### To Extend:
1. Add real database integration
2. Implement document storage
3. Add AI summarization with LLM
4. Integrate with hospital systems
5. Add comprehensive audit trails

---

## 📞 Support

For issues, see main documentation:
- [README.md](../README.md)
- [SYSTEM_ARCHITECTURE.md](../SYSTEM_ARCHITECTURE.md)
- [API_REFERENCE.md](../API_REFERENCE.md)

---

## ⏱️ Session Info

- **Login timeout:** 15 minutes
- **Session behavior:** Auto-logout on timeout
- **Token type:** Bearer token (demo mode)

---

**Demo Version:** 1.0
**Last Updated:** January 24, 2026
**Status:** Ready to run
