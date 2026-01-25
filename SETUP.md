# Project Setup Guide

## Quick Start

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

Backend runs on: http://localhost:5000

### Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

Frontend runs on: http://localhost:3000

### Database Setup

1. Create PostgreSQL database:
```sql
CREATE DATABASE patient_records;
```

2. Update DATABASE_URL in backend/.env

3. Run migrations:
```bash
cd backend
alembic upgrade head
```

## Testing

### Backend Tests
```bash
cd backend
pytest
pytest --cov=app tests/  # With coverage
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Development Workflow

1. Start backend: `python main.py` (port 5000)
2. Start frontend: `npm run dev` (port 3000)
3. Frontend proxy redirects API calls to backend
4. Open http://localhost:3000 in browser

## Demo Credentials

Username: `demo@hospital.com`
Password: `demo123`

## Deployment

See docs/DEPLOYMENT.md for production deployment procedures.
