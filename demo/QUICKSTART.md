# Quick Start Guide (Python 3.14)

Since you have Python 3.14 (which is newer than pydantic currently supports), use this simpler version:

## Backend Setup

```powershell
cd demo\backend

# Dependencies are already installed in venv!

# Run the server (using simplified version without pydantic)
venv\Scripts\python.exe main_simple.py
```

## Frontend Setup (New PowerShell window)

```powershell
cd demo\frontend

# Install dependencies
npm install

# Run the dev server
npm run dev
```

## Open Browser

Go to: **http://localhost:5173**

## Demo Credentials

- Doctor: `dr_johnson` / `demo123`
- Pharmacist: `pharm_smith` / `demo123`

## Demo Patients

- `PAT_987654` - John Smith (64M) - Full medical history
- `PAT_654321` - Mary Johnson (69F) - Simple case

---

## Notes

- The `main_simple.py` version works with Python 3.14
- All features are identical to the pydantic version
- Backend will run on: http://localhost:8000
- Frontend will run on: http://localhost:5173

---

## Troubleshooting

If npm is not found, make sure Node.js is installed and in your PATH.

Download from: https://nodejs.org/
