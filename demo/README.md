# AI-Patient-Record-Intelligence Demo

A fully functional demonstration of the doctor-first, safety-critical patient record system.

---

## Quick Start

### Windows (PowerShell)
```powershell
cd demo
.\start-demo.ps1
```

### macOS/Linux (Bash)
```bash
cd demo
chmod +x start-demo.sh
./start-demo.sh
```

The script will:
1. Check prerequisites (Python 3.9+, Node.js 16+)
2. Set up backend (create venv, install dependencies)
3. Set up frontend (install npm packages)
4. Start both servers
5. Open your browser to http://localhost:5173

---

## Manual Setup

### Backend (Terminal 1)

```bash
cd demo/backend

# Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
python main.py
```

**Backend runs on:** http://localhost:8000

### Frontend (Terminal 2)

```bash
cd demo/frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

**Frontend runs on:** http://localhost:5173

---

## Demo Credentials

### Doctors
- **Username:** `dr_johnson` / **Password:** `demo123` (DOCTOR)
- **Username:** `dr_hassan` / **Password:** `demo123` (DOCTOR)

### Pharmacist
- **Username:** `pharm_smith` / **Password:** `demo123` (PHARMACIST)

---

## Demo Patient Data

### Patient 1: John Smith (Main Demo)
- **Patient ID:** `PAT_987654`
- **Age:** 64 | DOB: 1960-05-15
- **Blood Type:** O+
- **Allergies:** Penicillin (CRITICAL), Sulfonamides, Latex
- **Chronic Conditions:** Type 2 Diabetes, Hypertension, Asthma
- **Implants:** Pacemaker (2019)
- **Current Meds:** Metformin 500mg, Lisinopril 10mg, Albuterol Inhaler

### Patient 2: Mary Johnson
- **Patient ID:** `PAT_654321`
- **Age:** 69 | DOB: 1955-08-22
- **Blood Type:** A-
- **Allergies:** Aspirin
- **Chronic Conditions:** Osteoarthritis

---

## Demo Workflow (3-4 minutes)

### 1. Login (0:00-0:30)
- Use: `dr_johnson` / `demo123`
- Observe: Role automatically detected (DOCTOR)

### 2. Patient Search (0:30-1:00)
- Search for: `PAT_987654`
- Results: John Smith (perfect match)
- Click: **Select Patient**

### 3. Patient Snapshot (1:00-2:00)
- Observe: ALL critical data visible (no scroll)
- Notice: Alert banner at top (Penicillin allergy)
- Left side: Stable data (locked, blood type, allergies)
- Right side: Dynamic data (medications, labs, timestamped)

### 4. Emergency Mode (2:00-2:30)
- Click: **🚨 Emergency Mode**
- Observe: Black background, large text, high contrast
- Data shows: Blood type, allergies, chronic conditions, meds
- Fast load: < 1 second

### 5. AI Summary (2:30-3:00)
- Go back to snapshot
- Click: **AI Summary**
- See: Structured data with source links
- Notice: Disclaimer about AI limitations

### 6. Role Switch (3:00-3:30)
- Logout
- Login as: `pharm_smith` / `demo123`
- View same patient: Different emphasis (medications focus)

---

## API Endpoints

### Authentication
```
POST /api/v1/auth/login
POST /api/v1/auth/logout
```

### Patient Search
```
GET /api/v1/patients/search?method=PATIENT_ID&value=PAT_987654
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

## Features Implemented

### Backend (FastAPI)
- Complete REST API (10+ endpoints)
- Authentication system (login/logout)
- Patient search (6 methods supported)
- Patient snapshot (main clinical view)
- Emergency mode (crisis mode)
- AI summary generation
- Role-based integration (Doctor/Pharmacist)
- Comprehensive demo data

### Frontend (React + Vite)
- Professional hospital UI
- Responsive design
- Hospital-grade color scheme
- All screens:
  - Login page
  - Patient search
  - Patient snapshot (main view)
  - Emergency mode (high contrast)
  - AI summary view
  - Role-based views

---

## Project Structure

```
demo/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── requirements.txt        # Python dependencies
│   └── .env.example           # Environment variables
│
├── frontend/
│   ├── src/
│   │   ├── main.jsx           # React entry point
│   │   ├── App.jsx            # Main app component
│   │   ├── App.css            # Main styles
│   │   ├── index.css          # Base styles
│   │   └── pages/
│   │       ├── Login.jsx
│   │       ├── PatientSearch.jsx
│   │       ├── PatientSnapshot.jsx
│   │       ├── EmergencyMode.jsx
│   │       └── AISummary.jsx
│   ├── index.html             # HTML template
│   ├── package.json           # Node dependencies
│   └── vite.config.js         # Vite configuration
│
├── README.md                  # This file
├── start-demo.ps1            # Windows startup script
└── start-demo.sh             # macOS/Linux startup script
```

---

## Troubleshooting

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
→ Solution: Ensure Python 3.14+
→ Solution: Run: pip install --upgrade pip
→ Solution: Run: pip install -r requirements.txt
```

---

## Key Demo Points

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

## Notes

- Demo uses in-memory data (no database)
- Tokens expire after 15 minutes
- All demo data is synthetic
- API responses mimic real hospital systems

---

## Security (Demo Only)

⚠️ **Note:** This is a **demo only**. Production would include:

- JWT tokens (not demo tokens)
- Bcrypt password hashing
- HTTPS/TLS encryption
- Comprehensive audit logging
- Database encryption
- HIPAA compliance validation

---

**Demo Version:** 1.0  
**Last Updated:** January 25, 2026  
**Status:** Ready to run
