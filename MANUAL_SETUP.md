# Manual Setup Guide

If the automatic `start-demo.ps1` script fails, follow these manual steps:

## Issue: Python 3.14 Compatibility

**Problem:** Python 3.14 is too new for pydantic 2.5.0  
**Solution:** Use Python 3.9-3.13 instead

### Option 1: Install Python 3.13

1. Download Python 3.13 from https://www.python.org/downloads/
2. Install it
3. Run the demo using `py -3.13` instead of `python`

### Option 2: Manual Setup with Python 3.13

#### Backend (Terminal 1)

```powershell
cd demo\backend

# Use Python 3.13 specifically
py -3.13 -m venv venv

# Activate
venv\Scripts\activate

# Install
pip install -r requirements.txt

# Run
python main.py
```

#### Frontend (Terminal 2)

```powershell
cd demo\frontend

# Install
npm install

# Run
npm run dev
```

#### Open Browser

Go to: http://localhost:5173

---

## Alternative: Docker Setup (Coming Soon)

If Python version issues persist, we can create a Docker setup that works with any host Python version.

---

## Quick Test

### Test Backend Only

```powershell
cd demo\backend
py -3.13 -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn
python -c "from fastapi import FastAPI; print('FastAPI works!')"
```

### Test if you have Python 3.13

```powershell
py -3.13 --version
```

If this fails, you need to install Python 3.13.

---

## Demo Credentials

- Doctor: `dr_johnson` / `demo123`
- Pharmacist: `pharm_smith` / `demo123`

## Demo Patients

- `PAT_987654` - John Smith (64M)
- `PAT_654321` - Mary Johnson (69F)
